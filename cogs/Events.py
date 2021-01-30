import discord
from discord.ext import commands
import random
import json
import re
from pysyllables import get_syllable_count

def remove_symbol(message):
    #list of chars to remove
    badCharsList = [';', ' ', '.', "'", '"', '!', '*', '_', '#', '~', '(', ')', '|', '{', '}', 
    '<', '>', '?', "\\", '/', '-', '+', '=', '^', '$', '&', '%' ',', '`', "’"]

    for symbol in badCharsList:
        if symbol in message:
            message = message.replace(symbol,"")
    
    return message

def remove_symbol_no_space(message):
    #list of chars to remove
    badCharsList = [';', '.', "'", '"', '!', '*', '_', '#', '~', '(', ')', '|', '{', '}', 
    '<', '>', '?', "\\", '/', '-', '+', '=', '^', '$', '&', '%' ',', '`', "’"]

    for symbol in badCharsList:
        if symbol in message:
            message = message.replace(symbol,"")
    
    return message

def remove_string(lst, message):
    messageList = message.strip().split(" ")
    for i in messageList:
        lst.remove(i)
    return lst




#List of f o r b i d d e n words
with open('badWords.json', 'r') as f:
    badWordsList = json.load(f)

#List of w characters
with open('wList.json', 'r', encoding='utf-8') as f:
    wList = json.load(f)

#FIXME: DELETE?
def Diff(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))


# def format_haiku(wordList, target=None):
#     #target = 5 if not target else target
#     final = ""
#     phrase = ""
#     count = 0
#     #count < target and word and len(wordList) > 0
#     if len(wordList) > 0 and count < target and wordList[0]:
#         currentWord = wordList[0]
#         #word = re.sub(currentWord, "", word, count=1)
#         wordList.remove(currentWord)
#         final += format_haiku(wordList, target - 1)
#         final += currentWord + " "
#         print(phrase)
#         if get_syllable_count(final) == 5 or get_syllable_count(final) == 7:
#             return final

#     return final

def format_haiku(lst, target=None):
    target = 5 if not target else target
    final = ""
    sylCount = 0
    for i in range(0,target):
        word = lst[i]
        sylCount += get_syllable_count(word)
        
        if (sylCount > target):
            break
        
        final += word + " "
    return final[0: len(final) - 1]
        




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
        combinations = [s for s in re.findall(r"\S[^\s\\]\S", message.content.lower())]
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
        set_combinations = set(combinations)
        combinedListCopy = combinedList
        combinations_not_in_set = list(set_combinations - set(combinedListCopy))
        combinedList = combinations + combinations_not_in_set
        
        #.find(lambda m: m.author.id == message.author.id)
        if self.i < 3 and message.author.id != self.bot:
            self.lastThreeContent += message.content
            self.i = self.i + 1
        if self.i == 3:
            combinedList.append(self.lastThreeContent)
            self.lastThreeContent = ""
            self.i = 0
        
        
        list_of_ws = wList["wList"]["ws"]
        for word in combinedList:
            if len(word) > 2:
                if isPalindrome(word) and middle_char(word) in list_of_ws:
                    uwuCount += 1
                elif middle_char(word) in list_of_ws:
                    uwuCount = uwuCount + 1
                else:
                    for s in complicatedUwUs:
                        s = remove_symbol(s)
                        if len(s) > 2 and isPalindrome(s):
                            uwuCount = uwuCount + 1
        
        if uwuCount > 0:
            SocialCredit = self.bot.get_cog('SocialCredit')
            await SocialCredit.remove_points(author_id, guild_id, uwuCount, message)
            uwuCount = 0
        
        #Haiku
        wordList = remove_symbol_no_space(message.content).strip().split(" ")
        print(wordList)
        syllableCount = 0
        for word in wordList:
            syllableCount += get_syllable_count(word)
        print(syllableCount)
        if syllableCount == 17:
            firstFiveSyllables = format_haiku(wordList, 5)
            wordList = remove_string(wordList, firstFiveSyllables)
            print(f"wordList = {wordList}")
            sevenSyllables = format_haiku(wordList, 7)
            wordList = remove_string(wordList, sevenSyllables)
            lastFiveSyllables = format_haiku(wordList, 5)

            #Create embed
            color = 0xC51D55
            embed = discord.Embed(color=color)
            embed.set_author(name="A Haiku:")
            test = '\u200b'
            embed.add_field(
                name=f'{test}',
                value=f"*{firstFiveSyllables}\n\n{sevenSyllables}\n\n{lastFiveSyllables}*",
                inline=False,
            )
            embed.set_footer(text=f"-{message.author.display_name}")
            await channel.send(embed=embed)
            
            



        
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
            await channel.send("is the process whereby organisms better adapted to their environment tend to survive and produce more offspring")
        
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
