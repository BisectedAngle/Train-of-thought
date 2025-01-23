import discord
import asyncio
from discord.ext import commands
from config import TOKEN
from nltk.corpus import words

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!tot ", intents=intents)

englishvocab = set(words.words())
checkword = False
prevword = ""
totlist = []
totlistlen = 1

suboink = 0
addoink = 0
froink = 0
boink = 0

waiting_gamestart = False
gamestartmessage_ID = 0
gamechannel = 0
gamehoster = ""

currplayer = 0
playerlist = []
lifelist = []

def halflength(word):       #half life gap
    return int(-(-len(word) // 2))

def checkboink(word1, word2):
    i=0
    while(word1[i]==word2[i]):
        i+=1
    if i>=halflength(word1):
        return True
    else:
        return False

def checkfroink(word1, word2):
    i=1
    while(word1[-i]==word2[-i]):
        i+=1
    if i-1>=halflength(word1):
        return True
    else:
        return False

def checkgoink(word,prevword):
    global totlist
    global suboink
    global addoink
    global froink
    global boink

    if word in totlist:
        return "WORDINLIST"
    else:
        if word in prevword:
            suboink+=1
            return "SUBOINK"
        elif prevword in word:
            addoink+=1
            return "ADDOINK"
        else:
            if checkfroink(prevword,word):
                froink +=1
                return "FROINK"
            elif checkboink(prevword,word):
                boink +=1
                return "BOINK"
            else:
                return ""

def iterateplayer(currplayer, playernum):
    if currplayer == playernum-1:
        return 0
    else:
        return currplayer+1
    
def getplayercolour(currplayer):
    if currplayer == 0:
        return discord.Colour.brand_red()
    if currplayer == 1:
        return discord.Colour.blue()
    if currplayer == 2:
        return discord.Colour.yellow()
    if currplayer == 3:
        return discord.Colour.brand_green()

def gettime(totlistlen):
    if totlistlen >= 15 and totlistlen < 25:
        return 10
    elif totlistlen >= 25 and totlistlen < 35:
        return 7
    elif totlistlen >= 35:
        return 5
    else:
        return 7
    

#----------------------------------------------------------------#

async def showtotlist():
    global totlist
    global winner
    global gamechannel

    global addoink
    global suboink
    global froink
    global boink

    totstring = totlist[0]
    for i in range(1,len(totlist)):
        totstring += f" → {totlist[i]}"
    
    embed = discord.Embed(
        colour=discord.Color.gold(),
        title=("TRAIN OF THOUGHT GAME STATS"),
        description=f"Winner: {winner}"
    )

    embed.add_field(name=f"{len(totlist)} words totted", value=totstring, inline=False)
    embed.add_field(name=f"ADDOINKS: {addoink}", value="", inline=True)
    embed.add_field(name=f"SUBOINKS: {suboink}", value="", inline=True)
    embed.add_field(name=f"FROINKS: {froink}", value="", inline=False)
    embed.add_field(name=f"BOINKS: {boink}", value="", inline=False)

    await gamechannel.send(embed=embed)




async def gameon():
    global playerlist
    global lifelist
    global gamechannel
    global prevword
    global word
    global englishvocab
    global checkword
    global currplayer
    global msg
    global totlistlen
    global winner
    global waiting_gamestart

    goinktype = ""
    timer = gettime(totlistlen)

    while True:
        embed = discord.Embed(
                colour=getplayercolour(currplayer),
                title=(prevword if totlistlen==1 else word)
            )
        
        embed.add_field(name="\n", value="", inline=False)
        embed.add_field(name="", value="{}'s turn! ".format(playerlist[currplayer]), inline=True)
        embed.add_field(name="", value=" Lives: {}".format(lifelist[currplayer]), inline=True)
        embed.add_field(name=" ", value=" ", inline=True)
        embed.add_field(name="Time before death: {}s".format(timer), value="", inline=True)
        
        if len(totlist)>1 and goinktype != "":
            embed.set_footer(text="{}!".format(goinktype))
            await msg.add_reaction('✅')
        
        sent = await gamechannel.send(embed=embed)

        if totlistlen>1:
            print(prevword,word)
            prevword = word
            goinktype = ""

        while goinktype == "" or goinktype == "WORDINLIST":
            embed = sent.embeds[0]

            while not checkword:

                while timer > 0:
                    try:
                        msg = await bot.wait_for('message',timeout=1)
                        break
                    except asyncio.TimeoutError:
                        timer -= 1
                        embed.set_field_at(3, name="Time before death: {}s".format(timer), value="", inline=False)
                        await sent.edit(embed=embed)
                

                if(msg.author.mention == playerlist[currplayer]):
                    word = (msg.content).lower()
                    checkword = word in englishvocab
                
                if timer == 0:
                    word = prevword
                    break
                
            
            if timer == 0:
                print("lose life")
                lifelist[currplayer] -= 1
                break

            goinktype = checkgoink(word,prevword)
            if goinktype == "":
                print("Not valid goink!")
            elif goinktype == "WORDINLIST":
                print("Word in list!")
                goinktype = ""
            checkword = False
        
        if lifelist[currplayer]==0:
            break
            
        if timer > 0:
            print(goinktype)
            totlist.append(word)
            totlistlen += 1
        
        currplayer = iterateplayer(currplayer,len(playerlist))
        print(totlistlen)
        timer = gettime(totlistlen)
    
    winner = playerlist[iterateplayer(currplayer,len(playerlist))]
    waiting_gamestart = False
    await showtotlist()


async def showplayerlist():
    global playerlist
    global lifelist
    global gamechannel

    embed = discord.Embed(
            colour=discord.Colour.gold(),
            title="TRAIN OF THOUGHT PLAYERS",
            description="🔴 "+playerlist[0]
        )
    if len(playerlist) >= 2:
        embed.description += "\n🔵 "+playerlist[1]
    if len(playerlist) >= 3:
        embed.description += "\n🟡 "+playerlist[2]
    if len(playerlist) == 4:
        embed.description += "\n🟢 "+playerlist[3]
    await gamechannel.send(embed=embed)
    await choosestart()


async def choosestart():
    global playerlist
    global gamechannel
    global prevword
    global englishvocab
    global checkword
    global currplayer
    global msg

    prevword = ""
    checkword = False
    embed = discord.Embed(
            colour=discord.Colour.red(),
            title='HOSTER CHOOSES THE STARTING WORD',
            description="{} Type it below and send it".format(playerlist[0])
        )
    await gamechannel.send(embed=embed)
    while not checkword:
        msg = await bot.wait_for('message')
        if(msg.author.mention == playerlist[currplayer]):
            prevword = (msg.content).lower()
            checkword = prevword in englishvocab
            if not checkword:
                await msg.reply("Not a real single word! (Please reinput)",mention_author=False)
    
    totlist.append(prevword)
    checkword = False
    currplayer = iterateplayer(currplayer,len(playerlist))
    await gameon()


#----------------------------------------------------------------#

@bot.event
async def on_ready():
    print("i just hopped")

@bot.command(name="start")
async def start(ctx):
    global waiting_gamestart
    global gamehoster
    global gamestartmessage_ID
    global gamechannel
    global playerlist
    global lifelist

    if waiting_gamestart == False:
        gamehoster = ctx.author
        print(gamehoster)

        waiting_gamestart = True
        embed = discord.Embed(
            colour=discord.Colour.gold(),
            title="TRAIN OF THOUGHT 🚂💭",
            description="Hoster: {} \n\nUp to 4️⃣ players\nReact with ✅ to join game \nThe hoster reacts with ▶️ to start game \n\nType '!tot rules' for game rules".format(gamehoster.mention)
        )

        startingmsg = await ctx.send(embed=embed)
        playerlist = [ctx.author.mention]
        lifelist = [3]
        print(playerlist)

        await startingmsg.add_reaction('▶️')
        await startingmsg.add_reaction('✅')
        gamestartmessage_ID = startingmsg.id
        gamechannel = startingmsg.channel

    else:
        await ctx.send("Game already pending/going!")

@bot.command(name="rules")
async def rules(ctx):
    embed = discord.Embed(
            colour=discord.Colour.gold(),
            description="im rules \nyes!",
            title="TRAIN OF THOUGHT GAME RULES 🚂❓"
        )
    await ctx.reply(embed=embed,mention_author=False)
    

@bot.event
async def on_reaction_add(reaction, user):
    global waiting_gamestart
    global gamehoster
    global gamestartmessage_ID
    global gamechannel
    global playerlist

    if user != bot.user:
        #TOT GAME STARTING MSG
        if reaction.message.id == gamestartmessage_ID:
            
            if str(reaction.emoji) == '✅':
                if (user != gamehoster) and (len(playerlist) < 4):
                    playerlist.append(user.mention)
                    lifelist.append(3)
                    await gamechannel.send('{} joined the game ({}/4)'.format(user.mention,len(playerlist)))
                elif user == gamehoster:
                    await gamechannel.send('You are already the game hoster!')
                    await reaction.message.remove_reaction('✅', user)
                elif len(playerlist)==4:
                    await gamechannel.send('Maximum players reached!')
                    await reaction.message.remove_reaction('✅', user)
            if str(reaction.emoji) == '▶️':
                if user == gamehoster:
                    await gamechannel.send('{} started the game!'.format(user.mention))
                    await showplayerlist()
                else:
                    await gamechannel.send('You are not the game hoster!')
                    await reaction.message.remove_reaction('▶️', user)


@bot.event
async def on_reaction_remove(reaction, user):
    global gamestartmessage_ID
    global gamehoster
    global playerlist

    if user != bot.user:
        if reaction.message.id == gamestartmessage_ID:
            channel = reaction.message.channel
            if str(reaction.emoji) == '✅':
                if user != gamehoster:
                    playerlist.remove(user.mention)
                    lifelist.pop(-1)
                    await channel.send('{} left the game ({}/4)'.format(user.mention,len(playerlist)))




bot.run(TOKEN)
    
    
