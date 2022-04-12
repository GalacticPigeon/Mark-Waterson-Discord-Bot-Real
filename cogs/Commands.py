import discord
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
import json
import re
import random
from math import log10, floor

#Function to check if a string contains any digit
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def remove_symbol(message):
    #list of chars to remove
    badCharsList = [';', ' ', '.', "'", '"', '!', '*', '_', '#', '~', '(', ')', '|', '{', '}', 
    '<', '>', '?', "\\", '/', '-', '+', '=', '^', '$', '&', '%' ',', '`', "’"]

    for symbol in badCharsList:
        if symbol in message:
            message = message.replace(symbol,"")
    
    return message

#List of f o r b i d d e n words
with open('badWords.json', 'r') as f:
    badWordsList = json.load(f)

class Commands(commands.Cog):
    """All commands that I had before my update (minus usersay)."""
    def __init__(self, bot):
        self.bot = bot

    #Version
    @commands.command()
    async def version(self, ctx):
        """Checks the fucking version. Do I even need to include this in help?"""
        await ctx.send('This is Mark Waterson bot Mk. 2.0!')

    # Ping command
    @commands.command()
    async def ping(self, ctx):
        """If you have to ask I'm removing your computer privelleges"""
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

    #Ask Mark/8ball commmand
    @commands.command(aliases=['8ball'])
    async def ask(self, ctx, *, question):
        """Ask Mark a question and he will answer you. usage: `_ask [question]`"""
        #Encoding (wrapper?) added to make program work. Unkown why I need this.
        with open('8ball.json', 'r', encoding='utf-8') as f:
            responseList = json.load(f)

        #load lists from json file
        responses = responseList['answers']['regular']
        yesList = responseList['answers']['yesList']
        noList = responseList['answers']['noList']
        
        #Print responses

        try:
            lst = [s for s in re.split(r'[^\d\W]+', question)]
            qstr = ''.join(str(e) for e in lst)
            qstr = qstr.replace('^', '**')
            lst = [s for s in re.split(r'[.?\-",]+', qstr)]
            lst = list(filter(None, lst))
            print(f"QSTR IS: {qstr}")
            qstr = ''.join(str(e) for e in lst)
            answer = eval(qstr)
            await ctx.send(f'Question: {question}\nAnswer: {answer}')
            return
        except:
            pass

        if hasNumbers(question):
            await ctx.send(f'Question: {question}\nAnswer: Don’t count on it.')

        elif 'will you listen' in question:
            await ctx.send(f"Question: {question}\nAnswer: I̸̛̙̞̦̠͎̯̩̬͙̯̮͔̔̓͛̔̓͂͂͋̽̅́́̂̄̆̓̿̕͘ ̴̢̡̨̨̭̝̟̮̥̯̣͖͍̖̝̲̳̺̐̂̾̅̐͛̊͊̀̄̓̏͛͗̀̉͗̽͒̕͝͠w̶̨̧̢̢̛͕̬̝̘̥͓͔͙͍̠͖̮̓̊͜i̷̧̨̧̡̢̙̹͚̼͎̳͓̗̲̦̭̭̺͈͈̰̯̲̦̺̽͑̄̽͌͛̿̋̀͒͑̓̓̐́͘̕̕̕ͅͅl̵̨̠͍͉͎̬̺͍̞̪͎͎̰̘̦̘͚̼̲̭͇͑͊̓̈̔̑̈́̐̌̇͐̌̄͑̄̓͐̚l̷̛̛̤̤̥̗̲̺̳͖̑̃̑̔̏͂̀̒̃͝͝ ̴̡̺͔̱̭̠̹͙̼̯̊̽̀͆́ņ̷͔̖͖̫̪̼̆̓̽͐̿͂̉̽̀̕̚͘͜o̴̺͎̙͓͈̫͚̹̼̳͚͐͌̋́͂̅͐ẗ̸̢̧̛͎̞̺̥͔̬̪̼̗͚̰́̃́̅́̏̐̈̓̉̆̅͒́̎̍̏͘͘͝͝͝ ̷̨͇̜̫̯̩̌̈͋͐̽̂̒̾͋̄́͆͋̚̕̚͠c̶͕̠͇̝̲̘͈̭̟̳̲̹̲͖̹̹̻̜͔͔̜̍͂͑͐̔̆͌̌̓̍̊̒͊͛̚͠͝ͅö̷̩͚̥͚͎͍̺͖̙̭̪͓̣̫̤̜̥̜̖̩̭͙͎́͐͋́͝m̴̛͙̼̹͔͍̃̽͋̔̆̊͑̅͒́͊ͅͅp̴̢̢̢̛̥̳̼̞̖̺̼͍͎̣̮͇͉͕͓̎̾͗̀͆̍̍́́̈̄͘͜l̴͓̦̭͍̼̉͒͋̓̕y̶̢̨̛̮̦̺͙͕̳̲̼͍̬͍̘̬̱̳̺̳̹̤̦̪̙͉͖͌̽͗́̅̊̃̈́̕͝͝ͅ")
        
        
        
        elif 'lie' in question and 'you' in question or 'lie' in question and 'mark' in question or 'lie' in question and 'Mark' in question:
            if 'never' in question:
                await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')
            else:
                await ctx.send(f'Question: {question}\nAnswer: {random.choice(noList)}')
        
        elif 'french' in question  and 'eliminated' in question or 'killed' in question or 'eradicated' in question or 'destroyed' in question or 'French' in question and 'eliminated' in question or 'killed' in question or 'eradicated' in question or 'destroyed' in question:
            await ctx.send(f'Question: {question}\nAnswer: {random.choice(yesList)}')
        else:
            await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    # Prints message if only an underscore is entered
    @commands.command(aliases=[''], hidden=True)
    async def test(self, ctx):
        """Ignore this command it isn't real"""
        await ctx.send("You need to type an actual command IDIOT")

    # J O H N
    @commands.command()
    async def john(self, ctx):
        """J O H N"""
        await ctx.send('https://i.imgur.com/TQZ7cAY.jpg')

    # This command make poopoo in pant
    @commands.command()
    async def poop(self, ctx):
        """This is a command"""
        if ctx.author.id != 527312390090522635:

            await ctx.send("░░░░░░░░░░░█▀▀░░█░░░░░")
            await ctx.send("░░░░░░▄▀▀▀▀░░░░░█▄▄░░░")
            await ctx.send("░░░░░░█░█░░░░░░░░░░▐░░")
            await ctx.send("░░░░░░▐▐░░░░░░░░░▄░▐░░")
            await ctx.send("░░░░░░█░░░░░░░░▄▀▀░▐░░")
            await ctx.send("░░░░▄▀░░░░░░░░▐░▄▄▀░░░")
            await ctx.send("░░▄▀░░░▐░░░░░█▄▀░▐░░░░")
            await ctx.send("░░█░░░▐░░░░░░░░▄░█░░░░")
            await ctx.send("░░░█▄░░▀▄░░░░▄▀▐░█░░░░")
            await ctx.send("░░░█▐▀▀▀░▀▀▀▀░░▐░█░░░░")
            await ctx.send("░░▐█▐▄░░▀░░░░░░▐░█▄▄░░")
            await ctx.send("░░░▀▀░░▄█▄░░░░░▐▄██▀░░")
    

    #Convert command
    @commands.command()
    async def convert(self, ctx, *, message):
        """Converts one measurement to another. usage: `_convert [measurement]` or `_convert [measurement] [measurement]`"""
        isConversion = False
        channel = ctx.message.channel
        new_message = remove_symbol(message.lower())
        #A list to display what conversions the user can make
        measurements = ["miles", "yards", "feet", "inches", "kilometers", "meters", "centimeters", "milimeters",
                        "mile", "yard", "foot", "inch", "kilometer", "meter", "centimeter", "milimeter",
                        "mi", "yd", "yds", "ft", "in", "km", "m", "cm", "mm"]

        #get units from message
        units = [word for word in message.split(" ") if word in measurements]

        #get numbers from message
        numbers = re.findall("\d+\.\d+", message)
        if len(numbers) < 1:
            numbers = [s for s in re.findall(r'\b\d+\b', message)]
            
        if len(numbers) > 1:
            await ctx.send("I can only convert one number at a time fuckwad")
            return
        elif len(numbers) < 1:
            await ctx.send("You have to enter a number fuckwad")
            return
        else:
            if ('.' in numbers[0]):
                numbers[0] = float(numbers[0])
            else:
                numbers[0] = int(numbers[0])
        number = numbers[0]

        #Converts number to penis
        def conv(number, units):
            yards_in_miles = 1760
            feet_in_miles = 5280
            kilometers_in_miles = 1.60934
            meters_in_kilometers = 1000
            centimeters_in_meters = 100
            milimeters_in_meters = 1000
            yards_in_feet = 3
            inches_in_feet = 12
            p_size_inches = 5.21

            if units[0] == "miles" or units[0] == "mile" or units[0] == "mi":
                number *= feet_in_miles
                number *= inches_in_feet
                number /= p_size_inches
            elif units[0] == "yards" or units[0] == "yard" or units[0] == "yd" or units[0] == "yds":
                number *= inches_in_feet * 3
                number /= p_size_inches
            elif units[0] == "feet" or units[0] == "foot" or units[0] == "ft":
                number *= inches_in_feet
                number /= p_size_inches
            elif units[0] == "inches" or units[0] == "inch" or units[0] == "in":
                number /= p_size_inches
            elif units[0] == "kilometers" or units[0] == "kilometer" or units[0] == "km":
                number /= kilometers_in_miles
                number = conv(number,["miles"])
            elif units[0] == "meter" or units[0] == "meters" or units[0] == "m":
                number /= 1000
                number = conv(number,["km"])
            elif units[0] == "centimeter" or units[0] == "centimeters" or units[0] == "cm":
                number /= 100
                number = conv(number,["m"])
            elif units[0] == "milimeter" or units[0] == "milimeters" or units[0] == "mm":
                number /= 1000
                number = conv(number, ["m"])

            return number

        #Rounds number to whatever significant digits entered
        #FIXME: change to 2 decimal places no matter what
        def round_to_digit(num, digit):
            answer = 0
            if (num != 0):
                answer = round(num, digit - int(floor(log10(abs(num)))) - 1)
            return answer

        if len(units) == 0:
            await ctx.send("That number is fucking naked I will not touch it")
            return
        oldNumber = number
        number = conv(number, units)
        number = round_to_digit(number, 3)

        if number == 1:
            await ctx.send("That number is one human penis!")
        elif number == 0:
            await ctx.send("There are no penises :pensive:")
        else:
            await ctx.send(f"{oldNumber} {units[0]} is approximately {number} human penises!")
        
    @commands.command()
    async def cchannel(self, ctx):
        #channel = discord.utils.get(ctx.guild.channels, name="memes")
        id = ctx.message.channel.id
        await ctx.send(f"CHANNEL ID IS LOOK HERE IT IS {id}")

    @commands.command()
    async def gguild(self, ctx):
        id = ctx.message.guild.id
        await ctx.send(id)

def setup(bot):
    bot.add_cog(Commands(bot))
