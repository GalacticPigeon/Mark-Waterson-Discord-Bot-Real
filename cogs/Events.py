import discord
from discord.ext import commands
import random
import json
import re
from pysyllables import get_syllable_count
from num2words import num2words



badCharsList = [';', '.', "'", '"', '!', '*', '_', '#', '~', '(', ')', '|', '{', '}', 
'<', '>', '?', "\\", '/', '-', '+', '=', '^', '$', '&', '%' ',', '`', "’", "@", "*"]

def remove_symbol(message):
    #list of chars to remove
    badCharsList = [';', ' ', '.', "'", '"', '!', '*', '_', '#', '~', '(', ')', '|', '{', '}', 
    '<', '>', '?', "\\", '/', '-', '+', '=', '^', '$', '&', '%' ',', '`', "’"]

    for symbol in badCharsList:
        if symbol in message:
            message = message.replace(symbol,"")
    
    return message


def sanitize_input(message):
    if (type(message) != 'list'): #If variable type is not a list
        for symbol in badCharsList:
            if symbol in message:
                if symbol.isnumeric():
                    pass
                else:
                    message = message.replace(symbol, symbol + " ")
    else:
        message = [message.replace(s, s + " ") for s in badCharsList]

    return message

#removes every piece of punctuation in the message
def remove_symbols(message):
    if (type(message) != 'list'): #If variable type is not a list
        for symbol in badCharsList:
            if symbol in message:
                if symbol.isnumeric():
                    pass
                else:
                    message = message.replace(symbol, symbol + "")
    else:
        message = [message.replace(s, s + "") for s in badCharsList]

    return message

def remove_string(lst, message):
    messageList = [s for s in re.split(r"\s+", message)]
    sanitize_input(message)
    messageList = list(filter(None, messageList))
    for i in messageList:
        lst.remove(i)
    return lst

def syllables(word):
    #referred from stackoverflow.com/questions/14541303/count-the-number-of-syllables-in-a-word
    count = 0
    vowels = 'aeiouy'
    word = word.lower()
    try:
        if word[0] in vowels:
            count +=1
        for index in range(1,len(word)):
            if word[index] in vowels and word[index-1] not in vowels:
                count +=1
        if word.endswith('e'):
            count -= 1
        if word.endswith('le'):
            count += 1
        if count == 0:
            count += 1
    except IndexError:
        pass
    return count


# #List of f o r b i d d e n words
with open('badWords.json', 'r') as f:
    badWordsList = json.load(f)

#List of w characters
with open('wList.json', 'r', encoding='utf-8') as f:
    wList = json.load(f)

with open('exclusions.json', 'r') as f:
    exclusions = json.load(f)

def format_haiku(lst):
    firstFive = []
    middleSeven = []
    lastFive = []
    final = [[], [], []]
    sylCount = 0
    k = 0
    i = 0
    for j in [5,7,5]:
        sylCount = 0
        while sylCount < j:
            try:
                word = lst[k]
            except Exception as e:
                pass
            sylCount += get_syl_count(remove_symbol(word))
            # This handles the case where the sum of syllables is 17
            # but the correct number of syllables per line cannot be formed
            # with the words
            if (sylCount > j):
                return None
            
            final[i].append(word)
            k += 1
        i += 1
    return final

#Gets the syllable count for ONE word and returns it
def get_syl_count(word):
    sylCount = 0
    syl_in_word = False
    word = remove_symbol(word)
    #print(f"WORD IS HEY HEY LOOK WORD IS {word}")
    try:
        if word.isnumeric():
            numList = [s for s in re.split(r"\s+|-+", num2words(word))]
            for string in numList:
                sylCount += get_syl_count(string)
            #print(f"sylCount = {sylCount}")
            #this is assigned to avoid calling an exception during recursion
            syl_in_word = True
        else:
            syl_in_word = get_syllable_count(word)
            sylCount = syl_in_word

        #Unsure why I have to raise an error here
        if not syl_in_word:
            raise Exception

    except Exception as BreakoutException:
        sylCount = 0
        #print(f"THIS IS THE WEIRD CASE WORD {word}")      
        if word.lower() in exclusions['exclusions']:
            sylCount = exclusions['exclusions'][word]
        else:
            sylCount += syllables(word)
    #typecast as a a bandaid instead of fixing this mess
    sylCount = int(sylCount)
    return sylCount

def listToStr(lst):
    string = " ".join([elem for elem in lst])
    return string

async def isBlock(self, str):
    if str == "_block":
        return [50, str.author.id]
    else:
        return [10, str.author.id]

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
        # ctx = await bot.get_ctx(message)

        # Gambling = self.bot.get_cog("Gambling")
        new_message = remove_symbol(message.content.lower())

        def isPalindrome(str):
            return str == str[::-1]
        
        def middle_char(txt):
            return txt[(len(txt)-1)//2:(len(txt)+2)//2]
        
        #TAXTAXTAXTAXTAXTAXTAXTAXTAXTAXTAXTAXTAXTAXTAXTAXTAXTAXTAXTAXTAX
        #Remove all symbols from message
        word = remove_symbols(message.content.lower())
        #Check if message has a taxed word
        with open('tax.json', 'r') as f:
            taxedWords = json.load(f)
        if word in taxedWords['taxedWords']:
            SocialCredit = self.bot.get_cog('SocialCredit')
            await SocialCredit.remove_points(author_id, guild_id, taxedWords['taxedWords'][word], message)
            embed = discord.Embed(
                color = discord.Color.red()
            )
            embed.set_author(name='haram')
            embed.add_field(name=f"\u200b", value=f"You have lost {taxedWords['taxedWords'][word]} UwU(s)", inline=False)
            await message.channel.send(embed=embed)

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
        
        #Haiku HAIKU HAIKU HAIKU HAIKU HAIKU HAIKU HAIKU HAIKU HAIKU HAIKU HAIKU HAIKU HAIKU HAIKU HAIKU HAIKU HAIKU HAIKU HAIKU HAIKU 
        #msg = []
        wordList = [s for s in re.split(r"\s+", message.content)]
        wordList = list(filter(None, wordList))
        wordList = sanitize_input(wordList)
        #print(wordList)
        syllableCount = 0
        for word in wordList:
            syllableCount += get_syl_count(word)

        #print(syllableCount)
        if syllableCount == 17:
            haiku = format_haiku(wordList)
            if (haiku is not None):
                firstFiveSyllables = listToStr(haiku[0])
                sevenSyllables = listToStr(haiku[1])
                lastFiveSyllables = listToStr(haiku[2])

                #Create embed
                color = 0xC51D55
                embed = discord.Embed(color=color)
                embed.set_author(name="A Haiku:")
                embed.add_field(
                    name='\u200b',
                    value=f"*{firstFiveSyllables}\n\n{sevenSyllables}\n\n{lastFiveSyllables}*",
                    inline=False,
                )
                embed.set_footer(text=f"-{message.author.display_name}")
                await channel.send(embed=embed)

        #Several message checks for phrases for bot to respond to
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

        
    
    #TODO: ADD ABILITY TO REMOVE WORDS
    @commands.command(hidden=True)
    @commands.is_owner()
    async def override(self, ctx, word, sylCount):
        with open('exclusions.json', 'r') as f:
            exclusions = json.load(f)
            
        word = str(word).lower()
        sylCount = int(sylCount)
        try:
            if word in exclusions['exclusions'] and exclusions['exclusions'][word] == sylCount:
                await ctx.send("Word already in exclusions!")
                return
            exclusions["exclusions"][word] = sylCount
            await ctx.send("Successfully added exception!")
            
            with open('exclusions.json', 'w') as f:
                json.dump(exclusions, f, indent=4)
        except Exception as e:
            await ctx.send("Failed to add word as an exception!")
            raise e
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def count(self, ctx, word):
        with open('exclusions.json', 'r') as f:
            exclusions = json.load(f)
        
        if word in exclusions['exclusions']:
            await ctx.send(f"{word} has {exclusions['exclusions'][word]}")
        else:
            count = get_syl_count(word)
            await ctx.send(f"{word} has {count} syllables!")

def setup(bot):
    bot.add_cog(Events(bot))
