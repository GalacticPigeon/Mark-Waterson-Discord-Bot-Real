import discord
from discord.ext import commands
import random
import json
import re

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

#List of w characters
with open('wList.json', 'r', encoding='utf-8') as f:
    wList = json.load(f)

class Events(commands.Cog):
    """No commands here no point in going here."""
    def __init__(self,bot):
        self.bot = bot
        
    lastThreeContent = ""
    i = 0

    # On Message Event
    @commands.Cog.listener()
    async def on_message(self,message):
        channel = message.channel #current channel
        isBadWords = False #boolean for bad words

        author_id = str(message.author.id)
        guild_id = str(message.guild.id)
        


        new_message = remove_symbol(message.content.lower())

        def isPalindrome(str):
            return str == str[::-1]
        
        def middle_char(txt):
            return txt[(len(txt)-1)//2:(len(txt)+2)//2]
        
        uwuCount = 0
        #Find all words that contain w
        ws = [s for s in re.findall(r'\S[Ww]\S', new_message)]
        complicatedUwUs = [s for s in re.findall(r'\S\s*[Ww]\s*\S', message.content.lower())]
        complicatedUwUs = [s.replace(' ', '') for s in complicatedUwUs]
        nonEnglish = [s for s in re.findall(r'[^\s\\][^\s\\][^\s\\]', new_message)]
        #(?i)[А-ЯЁ]
        for n, i in enumerate(ws):
                for m, j in enumerate(complicatedUwUs):
                    if len(i) <= 2:
                        ws[n] = complicatedUwUs[m]
        
        uwuCharacters = ["ⓦ", "⒲", "ഡ", "ധ", "ω", "ẁ", "ẃ", "ẅ", 
                        "ẇ", "ẉ", "ẘ", "ὠ", "ὡ", "ὢ", "ὣ", "ὤ", "ὥ", "ὦ", "ὧ", "ὼ", "ώ", "ᾠ", "ᾡ", 
                        "ᾢ", "ᾣ", "ᾤ", "ᾥ", "ᾦ", "ᾧ", "ῲ", "ῳ", "ῴ", "ῶ", "ῷ", "w", "₩", "Ẁ", "Ẃ", 
                        "Ẅ", "Ẇ", "Ẉ", "W", "ш", "ɰ"]
        set_ws = set(ws)
        set_compliUwUs = set(complicatedUwUs)
        complicatedUwUs_not_in_ws = list(set_compliUwUs - set_ws)
        combinedList = ws + complicatedUwUs_not_in_ws
        set_nonEnglish = set(nonEnglish)
        nonEnlish_not_in_set = list(set_nonEnglish - set(combinedList))
        combinedList = ws + nonEnlish_not_in_set
        
        #.find(lambda m: m.author.id == message.author.id)
        if self.i < 3 and message.author.id != self.bot.user:
            self.lastThreeContent += message.content
            self.i = self.i + 1
        if self.i == 3:
            combinedList.append(self.lastThreeContent)
            self.lastThreeContent = ""
            self.i = 0
        
        combinations = [s for s in re.findall(r"\S[^\s\\]\S", message.content.lower())]
        set_combinations = set(combinations)
        set_combinations_not_in_set = list(set_combinations - set(combinedList))
        combinedList = combinations + set_combinations_not_in_set
        list_of_ws = wList["wList"]["ws"]
        for word in combinedList:
            if len(word) > 2:
                if isPalindrome(word) and middle_char(word) in list_of_ws:
                    uwuCount += 1
                elif middle_char(word) in list_of_ws:
                    uwuCount = uwuCount + 1
                # else:
                #     for s in complicatedUwUs:
                #         s = remove_symbol(s)
                #         if len(s) > 2 and isPalindrome(s):
                #             uwuCount = uwuCount + 1
        
        if uwuCount > 0:
            SocialCredit = self.bot.get_cog('SocialCredit')
            await SocialCredit.remove_points(author_id, guild_id, uwuCount)
            uwuCount = 0

        
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
        
        if "mark" in new_message and "bigsoy" in new_message:
            await channel.send('👀')

        if 'why' in new_message:
            randNum = random.randint(0,5);
            if (randNum == 1):
                await channel.send('haram')

        
        #await bot.process_commands(message)

def setup(bot):
    bot.add_cog(Events(bot))
