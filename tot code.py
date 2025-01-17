import discord
from discord.ext import commands
from config import TOKEN
from nltk.corpus import words

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!tot ", intents=intents)

englishvocab = set(words.words())
checkword = False
prevword = ""
totlist = []

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
                

#----------------------------------------------------------------#

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

async def gameon():
    global playerlist
    global lifelist
    global gamechannel
    global prevword
    global word
    global englishvocab
    global checkword
    global currplayer

    goinktype = ""

    while True:
        while goinktype == "" or goinktype == "WORDINLIST":
            while not checkword:
                msg = await bot.wait_for('message')
                if(msg.author.mention == playerlist[currplayer]):
                    word = (msg.content).lower()
                    checkword = word in englishvocab
            goinktype = checkgoink(word,prevword)
            if goinktype == "":
                print("Not valid goink!")
            elif goinktype == "WORDINLIST":
                print("Word in list!")
                goinktype = ""
            checkword = False
        
        print(goinktype)
        totlist.append(word)
        currplayer = iterateplayer(currplayer,len(playerlist))

        embed = discord.Embed(
                colour=getplayercolour(currplayer),
                title=word,
                description="{}'s turn!         Lives: {}\n\n😵- - - - - - - - - - - - - - -🚂💭".format(playerlist[currplayer],lifelist[currplayer]))
        await msg.add_reaction('✅')
        await msg.reply(embed=embed,mention_author=False)
        
        print(prevword,word)
        prevword = word
        # checkword = False
        goinktype = ""


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
    embed = discord.Embed(
                colour=getplayercolour(currplayer),
                title=prevword,
                description="{}'s turn!                  Lives: {}\n😵- - - - - - - - - - - - - - -🚂💭".format(playerlist[currplayer],lifelist[currplayer]))
    
    await msg.add_reaction('✅')    
    await msg.reply(embed=embed,mention_author=False)

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
        lifelist = ["❤️❤️"]
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
                    lifelist.append("❤️❤️")
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
    
    
