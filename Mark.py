import discord
import json
import time
import os
import logging
import random
import aiohttp
from discord.ext import commands, tasks
from discord import member
from discord import Webhook, AsyncWebhookAdapter
from discord.utils import get
from itertools import cycle
from itertools import product
# from nltk.corpus import wordnet as wn
# import enchant

#TO DO: GO THROUGH USER MESSAGE HISTORY TO CHECK IF THEY INSULTED MARK WHILE BOT WAS OFFLINE

#global variable for the bad words list
global count #Used as a counter. Wouldn't let me use anything other than count
count = 0
global badWordsList1 #List of f o r b i d d e n words
badWordsList1 = ['kneegar',
                    'fuckass',
                    'erectile dysfunction',
                    'cialis',
                    'commit'
                    'comit'
                    'anal',
                    'anus',
                    'arse',
                    'ass'
                    'ass fuck',
                    'ass hole',
                    'assfucker',
                    'asshole',
                    'assshole',
                    'bastard',
                    'bitch',
                    'bad',
                    'black cock',
                    'bloody hell',
                    'boong',
                    'cock',
                    'cockfucker',
                    'cocksuck',
                    'cocksucker',
                    'coon',
                    'coom',
                    'doomer',
                    'coonnass',
                    'crap',
                    'cunt',
                    'cyberfuck',
                    'damn',
                    'darn',
                    'dick',
                    'dirty',
                    'douche',
                    'dummy',
                    'erect',
                    'erection',
                    'erotic',
                    'escort',
                    'fag',
                    'faggot',
                    'fuck',
                    'Fuck off',
                    'fuck you',
                    'fuckass',
                    'fuckhole',
                    'gay',
                    'god damn',
                    'gook',
                    'hard core',
                    'hardcore',
                    'homoerotic',
                    'hore',
                    'lesbian',
                    'lesbians',
                    'mother fucker',
                    'motherfuck',
                    'motherfucker',
                    'negro',
                    'nigger',
                    'orgasim',
                    'orgasm',
                    'penis',
                    'penisfucker',
                    'piss',
                    'piss off',
                    'porn',
                    'porno',
                    'pornography',
                    'pussy',
                    'retard',
                    'sadist',
                    'sex',
                    'sexy',
                    'shit',
                    'slut',
                    'son of a bitch',
                    'suck',
                    'tits',
                    'viagra',
                    'whore',
                    'woman',
                    'xxx', ]
    


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#Function to check if a string contains any digit
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

# Prefix for bot command
client = commands.Bot(command_prefix = '_')
client.remove_command('help')
status = cycle(['Absolute Vibes', 'with your mom lmao', 'Stuff', 'Currently facing east',])
#FIXME: COMMENT OUT
os.chdir(r'D:\Documents\Discord Bot')

#Tasks
@tasks.loop(seconds = 600)
async def change_status():
    await client.change_presence(activity = discord.Game(next(status)))

#load bad words list
#with open("badWords.txt", "r+") as badWords:
#    badWordsList = badWords.read().split()

#Helper function to filter out symbols in words
def remove_symbol(message):
     #list of chars to remove
     badCharsList = [';', ' ', '.', "'", '"', '!', '*', '_', '#', '~', '(', ')', '|', '{', '}', 
    '<', '>', '?', "\\", '/', '-', '+', '=', '^', '$', '&', '%' ',', '`', "’"]

    #  for symbol in badCharsList:
    #     if symbol in message:
    #         new_message = message.replace(symbol, '')
     for symbol in badCharsList:
         if symbol in message:
             message = message.replace(symbol,"")
    
     return message


# Events
@client.event
async def on_ready():
    change_status.start()
    print('Bot is ready!')


@client.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)
    
    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)
    
    print(f'{member} has joined a server!')

@client.event
async def on_member_remove():
    print(f'{member} has left a server.')

#Changes user nickname if they try to change name to Mark Waterson
@client.event
async def on_member_update(before, after):
    n = after.nick
    # user = member.display_name
    # print(user)
    if n:
        lower_n = n.lower()
        if 'mark' in lower_n or 'waterson' in lower_n or 'god' in lower_n or 'mee6' in lower_n:
            last = before.nick
            if last:
                await after.edit(nick = "lol u thought")
            else:
                await after.edit(nick = "lol u thought")

#Helper function to turn char array to string
def convert(s):
    new = ""
    for x in s:
        new += x
    return new

# On Message Event
@client.event
async def on_message(message):
    channel = message.channel #current channel
    isBadWords = False #boolean for bad words
    # d = enchant.Dict("en_US")


    
    global badWordsList1
    global count
    message_lower = message.content.lower()

    new_message = remove_symbol(message_lower)

    string_value = ",".join(badWordsList1)
    badWords = string_value.split(",")

    userSay = ['_usersay']

    for word in userSay:
        if word in message.content.lower():
            await message.channel.purge(limit=1)
    
    #FIXME: COMPLETE OR DELETE

    
    #END FIXME
    
    points = random.randint(-10,20)
    awardPoints = await reward_points()
    
    if (message.author.id != 697112219162247179 or message.author.id != 697460294573621278):
        with open('users.json', 'r') as f:
            users = json.load(f)
    
    
        await update_data(users, message.author)
        await add_points(users, message.author, points, awardPoints, message.channel)

        with open('users.json', 'w') as f:
            json.dump(users, f)
    
        

    for word in badWordsList1:
        if word in new_message:
            isBadWords = True
    
    if isBadWords and 'mark' in new_message or 'waterson' in new_message and isBadWords or 'waterboi' in new_message and isBadWords:
        await channel.send('No')

    if isBadWords and 'waterboy' in new_message:
        await channel.send('You think Adam Sandler is bad?')
    
    if 'hasno' in new_message and 'mark' in new_message or 'waterson' in new_message and 'hasno' in new_message:
        await channel.send('Yes I do.')

    if 'naturalselection' in new_message:
        await channel.send("Natural selection is the process whereby organisms better adapted to their environment tend to survive and produce more offspring")

    if 'whatsthedeal' in new_message or "whats the deal" in new_message:
        pts = await remove_points()
        with open('users.json', 'r') as f:
            users = json.load(f)
        await add_points(users, message.author, pts, True, message.channel)
        with open('users.json', 'w') as f:
            json.dump(users, f)
    
    #if message.author.display_name == "Robert Downey Jr.":
        # await channel.send('I am doing stuff')
    
    if 'whats' in new_message and '8ball' in new_message:
        await channel.send("8bol")
        
    if 'whats' in new_message and 'ping' in new_message:
        await channel.send('Nigga')

    # if 'mark' in new_message:
    #     await channel.send("Markalicous")

    if 'why' in new_message:
        randNum = random.randint(0,5);
        if (randNum == 1):
            await channel.send('haram')

        # role = discord.utils.get(message.author.roles, name = 'Peasants')
        # currentRole = get(message.author.roles, name='member')
        # await message.edit(roles = 'Peasants')
        # await discord.Member.add_roles(member, role)

    
    await client.process_commands(message)

#Update data helper function updates user data on message
async def update_data(users, user):
    if not str(user.id) in users:
        users[str(user.id)] = {}
        users[str(user.id)]['points'] = 0

# Helper function to add/remove points and displays message
async def add_points(users, user, pts, award, channel):
    if award:
        users[str(user.id)]['points'] += pts

    if award and pts >= 0:
        embed = discord.Embed(
            color = discord.Color.green()
        )
        embed.set_author(name='halal')
        embed.add_field(name='\u200b', value=f'you have gained {pts} point(s)', inline = False)
        await channel.send(embed=embed)
    
    if award and pts < 0:
        embed = discord.Embed(
            color = discord.Color.red()
        )
        embed.set_author(name='haram')
        embed.add_field(name='\u200b', value=f'you have lost {abs(pts)} point(s)', inline = False)
        await channel.send(embed=embed)

#Helper fucntion to determine whether or not to add points
async def reward_points():
    num = random.randint(0,100)

    if num == 1:
        return True
    else:
        return False

async def remove_points():
    pts = random.randint(-20,-1)
    return pts
    # users[str(user.id)]['points'] += pts
    # embed = discord.Embed(
    #         color = discord.Color.red()
    #     )
    # embed.add_field(name='haram', value=f'you have lost {abs(pts)} point(s)', inline = False)
    # await channel.send(embed=embed)


# Helper function to display number of points a user has
# async def disp_points(user):

#Deletes Every New Message
#@client.event
#async def on_message(message):
#    await message.delete()

# COMMANDS
#Help command
@client.command(pass_context = True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        color = discord.Color.blurple()
    )
    embed.set_author(name="Mark Waterson's friendly list of commands")
    embed.add_field(name='_version', value = 'Checks the fucking version. Do I even need to include this in help?', inline=False)
    embed.add_field(name='_ping', value="If you have to ask I'm removing your computer privelleges",inline=False)
    embed.add_field(name='_8ball', value = "It's a fucking 8ball what do you want me to say? Type the command and ask a question.", inline = False)
    embed.add_field(name='_stuff', value = "I am doing stuff", inline = False)
    embed.add_field(name='_john', value = "John", inline = False)
    embed.add_field(name='_usersay', value = "Type the command, @ someone, and type a phrase. Will make user say whatever you enter", inline = False)
    embed.add_field(name='_poop', value = "This is not a command", inline = False)
    embed.add_field(name='_points', value = "Checks how many points you currently have", inline = False)
    
    await ctx.send(embed=embed)

#Version
@client.command()
async def version(ctx):
    await ctx.send('This is Mark Waterson bot Mk. 1.16')

# Ping command
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

#8ball commmand
@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = [   'As I see it, yes.',
                    'Ask again later.',
                    'Better not tell you now.',
                    'Cannot predict now.',
                    'Concentrate and ask again.',
                    'Don’t count on it.',
                    'It is certain.',
                    'It is decidedly so.',
                    'Most likely.',
                    'My reply is no.',
                    'My sources say no.',
                    'Outlook not so good.',
                    'Outlook good.',
                    'Reply hazy, try again.',
                    'Signs point to yes.',
                    'Very doubtful.',
                    'Without a doubt.',
                    'Yes.',
                    'Yes – definitely.',
                    'You may rely on it.',
                    'I̸̛̙̞̦̠͎̯̩̬͙̯̮͔̔̓͛̔̓͂͂͋̽̅́́̂̄̆̓̿̕͘ ̴̢̡̨̨̭̝̟̮̥̯̣͖͍̖̝̲̳̺̐̂̾̅̐͛̊͊̀̄̓̏͛͗̀̉͗̽͒̕͝͠w̶̨̧̢̢̛͕̬̝̘̥͓͔͙͍̠͖̮̓̊͜i̷̧̨̧̡̢̙̹͚̼͎̳͓̗̲̦̭̭̺͈͈̰̯̲̦̺̽͑̄̽͌͛̿̋̀͒͑̓̓̐́͘̕̕̕ͅͅl̵̨̠͍͉͎̬̺͍̞̪͎͎̰̘̦̘͚̼̲̭͇͑͊̓̈̔̑̈́̐̌̇͐̌̄͑̄̓͐̚l̷̛̛̤̤̥̗̲̺̳͖̑̃̑̔̏͂̀̒̃͝͝ ̴̡̺͔̱̭̠̹͙̼̯̊̽̀͆́ņ̷͔̖͖̫̪̼̆̓̽͐̿͂̉̽̀̕̚͘͜o̴̺͎̙͓͈̫͚̹̼̳͚͐͌̋́͂̅͐ẗ̸̢̧̛͎̞̺̥͔̬̪̼̗͚̰́̃́̅́̏̐̈̓̉̆̅͒́̎̍̏͘͘͝͝͝ ̷̨͇̜̫̯̩̌̈͋͐̽̂̒̾͋̄́͆͋̚̕̚͠c̶͕̠͇̝̲̘͈̭̟̳̲̹̲͖̹̹̻̜͔͔̜̍͂͑͐̔̆͌̌̓̍̊̒͊͛̚͠͝ͅö̷̩͚̥͚͎͍̺͖̙̭̪͓̣̫̤̜̥̜̖̩̭͙͎́͐͋́͝m̴̛͙̼̹͔͍̃̽͋̔̆̊͑̅͒́͊ͅͅp̴̢̢̢̛̥̳̼̞̖̺̼͍͎̣̮͇͉͕͓̎̾͗̀͆̍̍́́̈̄͘͜l̴͓̦̭͍̼̉͒͋̓̕y̶̢̨̛̮̦̺͙͕̳̲̼͍̬͍̘̬̱̳̺̳̹̤̦̪̙͉͖͌̽͗́̅̊̃̈́̕͝͝ͅ'
                     ]

    if hasNumbers(question):
        await ctx.send(f'Question: {question}\nAnswer: Don’t count on it.')
    elif 'will you listen' in question:
        await ctx.send('I̸̛̙̞̦̠͎̯̩̬͙̯̮͔̔̓͛̔̓͂͂͋̽̅́́̂̄̆̓̿̕͘ ̴̢̡̨̨̭̝̟̮̥̯̣͖͍̖̝̲̳̺̐̂̾̅̐͛̊͊̀̄̓̏͛͗̀̉͗̽͒̕͝͠w̶̨̧̢̢̛͕̬̝̘̥͓͔͙͍̠͖̮̓̊͜i̷̧̨̧̡̢̙̹͚̼͎̳͓̗̲̦̭̭̺͈͈̰̯̲̦̺̽͑̄̽͌͛̿̋̀͒͑̓̓̐́͘̕̕̕ͅͅl̵̨̠͍͉͎̬̺͍̞̪͎͎̰̘̦̘͚̼̲̭͇͑͊̓̈̔̑̈́̐̌̇͐̌̄͑̄̓͐̚l̷̛̛̤̤̥̗̲̺̳͖̑̃̑̔̏͂̀̒̃͝͝ ̴̡̺͔̱̭̠̹͙̼̯̊̽̀͆́ņ̷͔̖͖̫̪̼̆̓̽͐̿͂̉̽̀̕̚͘͜o̴̺͎̙͓͈̫͚̹̼̳͚͐͌̋́͂̅͐ẗ̸̢̧̛͎̞̺̥͔̬̪̼̗͚̰́̃́̅́̏̐̈̓̉̆̅͒́̎̍̏͘͘͝͝͝ ̷̨͇̜̫̯̩̌̈͋͐̽̂̒̾͋̄́͆͋̚̕̚͠c̶͕̠͇̝̲̘͈̭̟̳̲̹̲͖̹̹̻̜͔͔̜̍͂͑͐̔̆͌̌̓̍̊̒͊͛̚͠͝ͅö̷̩͚̥͚͎͍̺͖̙̭̪͓̣̫̤̜̥̜̖̩̭͙͎́͐͋́͝m̴̛͙̼̹͔͍̃̽͋̔̆̊͑̅͒́͊ͅͅp̴̢̢̢̛̥̳̼̞̖̺̼͍͎̣̮͇͉͕͓̎̾͗̀͆̍̍́́̈̄͘͜l̴͓̦̭͍̼̉͒͋̓̕y̶̢̨̛̮̦̺͙͕̳̲̼͍̬͍̘̬̱̳̺̳̹̤̦̪̙͉͖͌̽͗́̅̊̃̈́̕͝͝ͅ')
    else:
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

# Prints message if only an underscore is entered
@client.command(aliases=[''])
async def test(ctx):
    await ctx.send("You need to type an actual command IDIOT")

# Prints I am doing stuff
@client.command()
async def stuff(ctx):
    await ctx.send('I am doing stuff')

# J O H N
@client.command()
async def john(ctx):
    await ctx.send('https://i.imgur.com/TQZ7cAY.jpg')

#WIP will make user say whatever text is entered
@client.command()
async def usersay(ctx, member: discord.Member = None, *, message):
    isBadWords = False #Checks if bad words in user mesasge
    channel = ctx.message.channel #channel variable
    Id = ctx.author.id #gets user id. Kinda useless
    myName = 'Galactic_Pigeon#2306' #The name of me
    leshenName = 'leshen_gang#7757' #The name of chip
    MEE6 = 'MEE6#4876' # The name of god
    mark = 'Mark Waterson#5554' # The name of the bot
    author = ctx.author.display_name #display the name of the message author
    authorAvatar = ctx.author.avatar_url #message author's avatar
    authorRealName = ctx.author.name #Name + tag of author
    mentioned = member or ctx.message.author # Either mentioned member or author if no mention is present
    memberName = member.display_name # Member nickname/name
    userName = ctx.message.author # Member acutal name + member tag
    avatar = member.avatar_url # Member avatar
    file = 'badWords2.txt'
    
    badWordsList = ['kneegar',
                    'fuckass',
                    'erectile dysfunction',
                    'cialis',
                    'anal',
                    'anus',
                    'arse',
                    'ass'
                    'ass fuck',
                    'ass hole',
                    'assfucker',
                    'asshole',
                    'assshole',
                    'bastard',
                    'bitch',
                    'black cock',
                    'bloody hell',
                    'boong',
                    'cock',
                    'cockfucker',
                    'cocksuck',
                    'cocksucker',
                    'coon',
                    'coom',
                    'doomer',
                    'coonnass',
                    'crap',
                    'cunt',
                    'cyberfuck',
                    'damn',
                    'darn',
                    'dick',
                    'dirty',
                    'douche',
                    'dummy',
                    'erect',
                    'erection',
                    'erotic',
                    'escort',
                    'fag',
                    'faggot',
                    'fuck',
                    'Fuck off',
                    'fuck you',
                    'fuckass',
                    'fuckhole',
                    'gay',
                    'god damn',
                    'gook',
                    'hard core',
                    'hardcore',
                    'homoerotic',
                    'hore',
                    'lesbian',
                    'lesbians',
                    'mother fucker',
                    'motherfuck',
                    'motherfucker',
                    'negro',
                    'nigger',
                    'orgasim',
                    'orgasm',
                    'penis',
                    'penisfucker',
                    'piss',
                    'piss off',
                    'porn',
                    'porno',
                    'pornography',
                    'pussy',
                    'retard',
                    'sadist',
                    'sex',
                    'sexy',
                    'shit',
                    'slut',
                    'son of a bitch',
                    'suck',
                    'tits',
                    'viagra',
                    'whore',
                    'woman',
                    'xxx',
                    'is making',
                    'has no',
                    'mark',
                    'neckrope' 
                    'neck rope',
                    'Mark Waterson#5554',
                    'shitting',
                    'cumming',
                    'moron']
    
    #Does stuff with list to make it work.
    string_value = ",".join(badWordsList)
    badWords = string_value.split(",")

    messageStr = str(message)
    messageStrLower = messageStr.lower()
    authorRealNameStr = str(authorRealName)

    messageStrLower = remove_symbol(messageStrLower)

    for word in badWordsList:
        if word in messageStrLower:
                isBadWords = True
    
    if isBadWords and str(userName) != myName:
        if str(mentioned) == mark or myName:
            avatar = authorAvatar
            memberName = author

    if "@everyone" in messageStrLower and str(userName) != myName:
        message = "no"
            

    #Webhook
    # async with aiohttp.ClientSession() as session:
    #     #webhook = Webhook.from_url('https://discordapp.com/api/webhooks/702199447110680586/fiWYrV9_IjdEcdI8d2MQZyuVZO5_YdNmr0YC4F2Z1epW7cIUr03vbHXrsYr-gotW-id2', adapter=AsyncWebhookAdapter(session))
    #     Webhook.avatar_url = avatar
    #     await webhook.send(message, username = memberName, avatar_url = avatar)

    #Webhook V2
    Webhook.avatar_url = avatar
    webhook = await channel.create_webhook(name = memberName)
    await webhook.send(message, username = memberName, avatar_url = avatar)
    await webhook.delete()

# Points command displays user's points
@client.command()
async def points(ctx, member: discord.Member = None):
    channel = ctx.channel
    user = ctx.author.id
    author = ctx.author.display_name
    with open('users.json', 'r') as f:
        users = json.load(f)
    # await ctx.send("There is currently no way to check your points until I, Mark Waterson, deem it so")
    # await ctx.send(f"You have {users[str(user)]['points']} points")

    if(users[str(user)]['points'] > 0):
        embed = discord.Embed(
        color = discord.Color.green()
        )
        embed.set_author(name=author)
        embed.add_field(name='\u200b', value = f"You have {users[str(user)]['points']} points", inline=False)
        await ctx.send(embed=embed)
    elif(users[str(user)]['points'] == 0):
        embed = discord.Embed(
            color = discord.Color.light_grey()
        )
        embed.set_author(name=author)
        embed.add_field(name='\u200b', value = f"You have {users[str(user)]['points']} points", inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
        color = discord.Color.red()
        )
        embed.set_author(name=author)
        embed.add_field(name='\u200b', value = f"You have {users[str(user)]['points']} points", inline=False)
        await ctx.send(embed=embed)


@client.command()
async def mark(ctx, member: discord.Member = None):
    if(ctx.author.id == 310162848254787585):
        #await client.create_guild("Mark Waterson",region=None,icon=None)
        perms = discord.Permissions()
        role = await ctx.guild.create_role(name="Mark Waterson", reason=None)
        await ctx.channel.set_permissions(role, mention_everyone=True)
        await ctx.send("Mark")
    else:
        ctx.send("Mark")

client.run('Njk3MTEyMjE5MTYyMjQ3MTc5.XoyiWA.cn02llCxi_bU427lSMva1ZKzACY')
