import discord
import json
import time
import os
from os import listdir
from os.path import isfile, join
import logging
import random
import aiohttp
import asyncpg
import re
import traceback
from discord.ext import commands, tasks
from discord import member
from discord.utils import get
from itertools import cycle
from itertools import product
from itertools import chain

#List of f o r b i d d e n words
with open('badWords.json', 'r') as f:
    badWordsList = json.load(f)


# Prefix for bot command
client = commands.Bot(command_prefix = '_')
client.remove_command('help')
status = cycle(['Absolute Vibes', 'with your mom lmao', 'Stuff', 'Currently facing east',])
#FIXME: COMMENT OUT
#os.chdir(r'D:\Documents\Discord Bot')

#Create database
async def create_db_pool():
    #await asyncpg.connect("postgres://dhluktlzulnova:89f3456ec09daac00209556799f98a896b2055fc02af3c8491db47406b41e86a@ec2-23-23-36-227.compute-1.amazonaws.com:5432/dao8a0cgglvabc?ssl=true")
    client.pg_con = await asyncpg.create_pool(database="dao8a0cgglvabc", user="dhluktlzulnova", password="89f3456ec09daac00209556799f98a896b2055fc02af3c8491db47406b41e86a")

#Tasks
@tasks.loop(seconds = 600)
async def change_status():
    await client.change_presence(activity = discord.Game(next(status)))

#Helper function to filter out symbols in words
def remove_symbol(message):
     #list of chars to remove
     badCharsList = [';', ' ', '.', "'", '"', '!', '*', '_', '#', '~', '(', ')', '|', '{', '}', 
    '<', '>', '?', "\\", '/', '-', '+', '=', '^', '$', '&', '%' ',', '`', "’"]

     for symbol in badCharsList:
         if symbol in message:
             message = message.replace(symbol,"")
    
     return message


# Events
@client.event
async def on_ready():
    change_status.start()
    print('Bot is ready!')

#Changes user nickname if they try to change name to Mark Waterson
@client.event
async def on_member_update(before, after):
    n = after.nick
    if n:
        lower_n = n.lower()
        if 'mark' in lower_n or 'waterson' in lower_n or 'god' in lower_n or 'mee6' in lower_n:
            last = before.nick
            if last:
                await after.edit(nick = "lol u thought")
            else:
                await after.edit(nick = "lol u thought")


#COGSCOGSCOGSCOGSCOGSCOGSCOGSCOGSCOGSCOGSCOGSCOGSCOGSCOGSCOGSCOGSCOGSCOGSCOGSCOGSCOGSCOGSCOGSCOGSCOGSCOGS
# for cog in cog:
#    if cog.endswith(".py") and not cog.startswith("_"):
#        try:
#            cogs = f"cogs.{cog.replace('.py','')}"
#            client.load_extension(cogs)
#        except Exception as e:
#            print(f"{cog} failed to load:")
#            raise e
cogs_dir = "cogs"
if __name__ == '__main__':
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        if not extension.startswith("_"):
            try:
                print(cogs_dir + "." + extension)
                client.load_extension(cogs_dir + "." + extension)
            except (discord.ClientException, ModuleNotFoundError):
                print(f'Failed to load extension {extension}.')

#Reload Cog Command
@client.command(hidden=True)
@commands.is_owner()
async def reload(ctx, cog):
    """Owner only command do not concern yourself mortal"""
    try:
        client.unload_extension(f"cogs.{cog}")
        client.load_extension(f"cogs.{cog}")
        await ctx.send(f"{cog} has been reloaded!")
    except Exception as e:
        print(f"{cog} cannot be loaded:")
        raise e

#Will make user say whatever text is entered
@client.command()
async def usersay(ctx, member: discord.Member = None, *, message):
    """Type the command, @ someone, and type a phrase. Will make user say whatever you enter `_usersay [member] [message]`"""
    isBadWords = False #Checks if bad words in user mesasge
    channel = ctx.channel #channel variable
    myName = 'Galactic_Pigeon#2306' #The name of me
    mark = 'Mark Waterson#5554' # The name of the bot
    author = ctx.author.display_name #display the name of the message author
    authorAvatar = ctx.author.avatar_url #message author's avatar
    member = ctx.author.display_name if not member else member
    mentioned = str(member) or str(ctx.message.author) # Either mentioned member or author if no mention is present
    memberName = member.display_name # Member nickname/name
    userName = str(ctx.message.author) # Member acutal name + member tag
    avatar = member.avatar_url # Member avatar
    #message = "SHOULD NOT SEE THIS" if not message else message
    messageStrLower = remove_symbol(message.lower())
    

    #Get rid of user message
    #note delete_afer(5)
    try:
        await channel.purge(limit=1)
    except:
        pass

    #look for bad word in message
    for word in badWordsList['badWords']['words']:
        if word in messageStrLower:
                isBadWords = True
    
    if isBadWords:
        if mentioned == mark or myName:
            avatar = authorAvatar
            memberName = author

    #Make it so Mark cannot @ everyone
    if "@everyone" in messageStrLower and userName != myName:
        message = "no"


    #Webhook V2
    Webhook.avatar_url = avatar
    webhook = await channel.create_webhook(name = memberName)
    await webhook.send(message, username = memberName, avatar_url = avatar)
    await webhook.delete()

#Run database
client.loop.run_until_complete(create_db_pool())


client.run('Njk3MTEyMjE5MTYyMjQ3MTc5.XoyiWA.cn02llCxi_bU427lSMva1ZKzACY')
