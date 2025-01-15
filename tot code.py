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
currplayer = 0

waiting_gamestart = False
gamestartmessage_ID = 0
gamechannel = 0
gamehoster = ""
playerlist = []
lifelist = []

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
    while True:
        while not checkword:
            msg = await bot.wait_for('message')
            if(msg.author.mention == playerlist[currplayer]):
                word = (msg.content).lower()
                checkword = word in englishvocab
                if not checkword:
                    await msg.reply("Not a real single word! (Please reinput)",mention_author=False)
        totlist.append(word)
        checkword = False
        currplayer = iterateplayer(currplayer,len(playerlist))

        embed = discord.Embed(
                colour=getplayercolour(currplayer),
                title=word,
                description="{}'s turn!".format(playerlist[currplayer]))
        
        print(prevword,word)
        await msg.reply(embed=embed,mention_author=False)
        prevword = word


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
                description="{}'s turn!".format(playerlist[currplayer]))
        
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
        lifelist = [2]
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
                    lifelist.append(2)
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
    
    
