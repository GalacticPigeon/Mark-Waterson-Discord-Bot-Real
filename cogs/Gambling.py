import discord
from discord.ext import commands

import random
import asyncio

# def moneyparser(money):
#     money = str(money)
#     nmoney = ""
#     if money.endswith("000000000000000"):
#         nmoney = money[:-15] + "Q"
#     elif money.endswith("000000000000"):
#         nmoney = money[:-12] + "T"
#     elif money.endswith("000000000"):
#         nmoney = money[:-9] + "B"
#     elif money.endswith("000000"):
#         nmoney = money[:-6] + "M"
#     elif money.endswith("000"):
#         nmoney = money[:-3] + "K"
#     else:
#         nmoney = money

#     if int(money) >= 1000000000:
#         nmoney += " 💴"
#     elif int(money) >= 1000000: 
#         nmoney += " 💷"
#     elif int(money) >= 1000:
#         nmoney += " 💰"
#     else:
#         nmoney += " 💵"
#     return nmoney

# def moneyunparser(money):
#     money = str(money).lower()
#     nmoney = ""
#     if money.isdigit():
#         return int(money)
#     else:
#         if not money[:-1].isdigit():
#             return
#     if money.endswith("q"):
#         nmoney = money[:-1] + "000000000000000"
#     elif money.endswith("t"):
#         nmoney = money[:-1] + "000000000000"
#     elif money.endswith("b"):
#         nmoney = money[:-1] + "000000000"
#     elif money.endswith("m"):
#         nmoney = money[:-1] + "000000"
#     elif money.endswith("k"):
#         nmoney = money[:-1] + "000"
#     else:
#         nmoney = money

#     return int(nmoney)

def remove_symbol(message):
    #list of chars to remove
    badCharsList = [';', ' ', '.', "'", '"', '!', '*', '_', '#', '~', '(', ')', '|', '{', '}', 
    '<', '>', '?', "\\", '/', '-', '+', '=', '^', '$', '&', '%' ',', '`', "’"]

    for symbol in badCharsList:
        if symbol in message:
            message = message.replace(symbol,"")
    
    return message


class Gambling(commands.Cog):
    """Gamble your UwUs and potentially become rich!"""
    def __init__(self, bot):
        self.bot = bot
    

    
    # @commmands.command(aliases=['rr'])
    # async def russianroulette(self, ctx, bet_amount: str, bullet_count: int):
    #     return
    
    @commands.command(aliases=['toss', 'ct', 'flip'])
    async def cointoss(self, ctx, heads_or_tails: str = None, bet_amount: str = None):
        """Toss a coin and make a bet! You could win big! usage: `_cointoss [heads or tails] [amount]`"""
        author_id = str(ctx.author.id) 
        guild_id = str(ctx.guild.id)
        result = random.randint(0, 1)
        user = await self.bot.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)
        num_uwus = user[0]['uwus']
        bet_amount = heads_or_tails if not bet_amount and heads_or_tails.isdigit() else bet_amount
        bet_amount = "1" if not bet_amount else bet_amount
        heads_or_tails = "heads" if heads_or_tails.isdigit() else heads_or_tails
        

        heads_or_tails = heads_or_tails.lower()
        
        if heads_or_tails.startswith('h'):
            heads_or_tails = 'heads'
        elif heads_or_tails.startswith('t'):
            heads_or_tails = 'tails'

        
        isNumber = False
        if bet_amount.isdigit():
            bet_amount = int(bet_amount)
            isNumber = True
        else:
            await ctx.send("How tf am I supposed to bet that? Enter a whole number")
            return


        if bet_amount == 0:
            await ctx.send("You can't bet nothing stupid")
            return
        elif bet_amount < 0:
            await ctx.send("You can't bet less than nothing stupid")
            return
        elif bet_amount > num_uwus:
            await ctx.send("You can't bet more than you have IDIOT")
            return
        
        await ctx.send(f"**{ctx.author.display_name}** called **{heads_or_tails}** and bet **{bet_amount}** *UwU(s)*")
        await ctx.send("*Tossing coin...*") #Add animation here later?
        await asyncio.sleep(2)

        bet_amount = abs(bet_amount)
        bet_amount = round(bet_amount * 1.5)
        if result == 0 and heads_or_tails == 'heads':
            await ctx.send(f"They won **{bet_amount}** UwU(s)!")
        elif result == 1 and heads_or_tails == 'tails':
            await ctx.send(f"They won **{bet_amount}** UwU(s)!")
        else:
            bet_amount = round((bet_amount / 1.5) * -1)
            await ctx.send(f"They lost **{abs(bet_amount)}** UwU(s)!")

        await self.bot.pg_con.execute("UPDATE users SET uwus = $1 WHERE user_id = $2 AND guild_id = $3", user[0]['uwus'] + bet_amount, author_id, guild_id)
    
    
    @commands.command(aliases=['donate', 'send'])
    async def give(self, ctx, member: discord.Member = None, amount="1"):
        """Give a user some UwUs You generous bastard you! usage: `_give [user] [amount]`"""
        member = ctx.author if not member else member
        author_id = str(ctx.author.id) 
        guild_id = str(ctx.guild.id)
        member_id = str(member.id)

        if amount.isdigit():
            amount = int(amount)
        else:
            await ctx.send(f"You can't send {amount} UwUs idiot")
            return


        user = await self.bot.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)

        if (member_id == author_id):
            await ctx.send(f"**{ctx.author.display_name}** just sent ***__{amount}__*** UwU(s) to **{member.display_name}**! How kind and generous! They must be proud!")
        else:
            #Take UwUs from user
            await self.bot.pg_con.execute("UPDATE users SET uwus = $1 WHERE user_id = $2 AND guild_id = $3", user[0]['uwus'] - amount, author_id, guild_id)
            #Add UwUs to member
            await self.bot.pg_con.execute("UPDATE users SET uwus = $1 WHERE user_id = $2 AND guild_id = $3", user[0]['uwus'] + amount, member_id, guild_id)
            await ctx.send(f"**{ctx.author.display_name}** just sent ***__{amount}__*** UwU(s) to **{member.display_name}**!")
    
    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        """I give you your daily dose of delicious dopamine with this command! It's free UwUs! usage: `_daily`"""
        author_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        user = await self.bot.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)
        num_uwus = user[0]['uwus']
        if (num_uwus < 0):
            amount = random.randint(abs(num_uwus), abs(num_uwus) + 10)
        else:
            amount = random.randint(10, 50)
        
        await self.bot.pg_con.execute("UPDATE users SET uwus = $1 WHERE user_id = $2 AND guild_id = $3", user[0]['uwus'] + amount, author_id, guild_id)
        await ctx.send(f"**{ctx.author.display_name}**, Here is your daily allowance of **{amount}** UwUs from ***__Mark Waterson__***")

        







def setup(bot):
    bot.add_cog(Gambling(bot))
