import discord
from discord.ext import commands

import json

def moneyparser(money):
    money = str(money)
    nmoney = ""
    if money.endswith("000000000000000"):
        nmoney = money[:-15] + "Q"
    elif money.endswith("000000000000"):
        nmoney = money[:-12] + "T"
    elif money.endswith("000000000"):
        nmoney = money[:-9] + "B"
    elif money.endswith("000000"):
        nmoney = money[:-6] + "M"
    elif money.endswith("000"):
        nmoney = money[:-3] + "K"
    else:
        nmoney = money

    if int(money) >= 1000000000:
        nmoney += " 💴"
    elif int(money) >= 1000000: 
        nmoney += " 💷"
    elif int(money) >= 1000:
        nmoney += " 💰"
    else:
        nmoney += " 💵"
    return nmoney

def moneyunparser(money):
    money = str(money).lower()
    nmoney = ""
    if money.isdigit():
        return int(money)
    else:
        if not money[:-1].isdigit():
            return
    if money.endswith("q"):
        nmoney = money[:-1] + "000000000000000"
    elif money.endswith("t"):
        nmoney = money[:-1] + "000000000000"
    elif money.endswith("b"):
        nmoney = money[:-1] + "000000000"
    elif money.endswith("m"):
        nmoney = money[:-1] + "000000"
    elif money.endswith("k"):
        nmoney = money[:-1] + "000"
    else:
        nmoney = money

    return int(nmoney)

class Gambling(commands.Cog):
    def __init__(self, bot):
        bot = self.bot



def setup(bot):
    bot.add_cog(Gambling(bot))
