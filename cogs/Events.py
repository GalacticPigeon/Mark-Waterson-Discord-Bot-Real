import discord
from discord.ext import commands
import random
import json

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

class Events(commands.Cog):
    """No commands here no point in going here."""
    def __init__(self,bot):
        self.bot = bot

    # On Message Event
    @commands.Cog.listener()
    async def on_message(self,message):
        channel = message.channel #current channel
        isBadWords = False #boolean for bad words

        new_message = remove_symbol(message.content.lower())
        
        
        for word in badWordsList['badWords']['words']:
            if word in new_message:
                isBadWords = True
        
        if 'mark' in new_message and isBadWords or 'waterson' in new_message and isBadWords or 'waterboi' in new_message and isBadWords:
            await channel.send('No')

        if isBadWords and 'waterboy' in new_message:
            await channel.send('You think Adam Sandler is bad?')
        
        if 'hasno' in new_message and 'mark' in new_message or 'waterson' in new_message and 'hasno' in new_message:
            await channel.send('Yes I do.')

        if 'naturalselection' in new_message:
            await channel.send("Natural selection is the process whereby organisms better adapted to their environment tend to survive and produce more offspring")
        
        if 'whats' in new_message and '8ball' in new_message:
            await channel.send("8bol")
            
        if 'whats' in new_message and 'ping' in new_message:
            await channel.send('Bruh')

        if 'why' in new_message:
            randNum = random.randint(0,5);
            if (randNum == 1):
                await channel.send('haram')

        
        #await bot.process_commands(message)

def setup(bot):
    bot.add_cog(Events(bot))