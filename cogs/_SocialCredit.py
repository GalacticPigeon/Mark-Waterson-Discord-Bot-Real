import discord
from discord.ext import commands

import json
import random
import asyncio

class SocialCredit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open('new_users.json', 'r') as f:
            self.users = json.load(f)
        
        



    def change_lvl(self, author_id):
        curr_uwus = self.users[author_id]['UwUs']
        curr_social_credit = self.users[author_id]['Social Credit']

        if curr_uwus >= (4 * round((curr_social_credit ** 3)) / 5):
            self.users[author_id]['Social Credit'] += 1
            return True
        elif curr_uwus <= (-4 * round((curr_social_credit ** 3)) / 5):
            self.users[author_id]['Social Credit'] -= 1
            return True
        else:
            return False


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.id == 697112219162247179:
            return

        author_id = str(message.author.id)

        with open('new_users.json', 'r') as f:
            self.users = json.load(f)

        if not author_id in self.users:
            self.users[author_id] = {}
            self.users[author_id]['Social Credit'] = 1
            self.users[author_id]['UwUs'] = 0

        def reward_points():
            num = random.randint(0,0)

            if num == 0:
                return True
            else:
                return False
        

        if reward_points():
            self.users[author_id]['UwUs'] += random.randint(-1, 2)



        if self.change_lvl(author_id):
            embed = discord.Embed(
                color = discord.Color.orange()
            )
            embed.set_author(name=message.author.display_name, icon_url=ctx.author.avatar_url)
            embed.add_field(name='\u200b', value=f"{message.author.display_name} now has a Social Credit of {self.users[author_id]['Social Credit']}", inline = False)
            await message.channel.send(embed=embed)

        with open('new_users.json', 'w') as f:
            json.dump(self.users, f, indent = 4)
    


    
    @commands.command(aliases=['uwus'])
    async def credit(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        member_id = str(member.id)

        if not member_id in self.users:
            embed = discord.Embed(
                color = discord.Color.light_grey()
            )
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            embed.add_field(name=f'Social Credit - {member.display_name}', value="No Social Credit", inline = False)
            await ctx.channel.send(embed=embed)
        else:
            if self.users[member_id]['Social Credit'] > 0:
                embed = discord.Embed(
                    color = discord.Color.green()
                )
                embed.set_author(name=member.display_name, icon_url=ctx.author.avatar_url)
                embed.add_field(name=f"UwUs - {member.display_name}", value=self.users[member_id]['UwUs'], inline=False)
                embed.add_field(name=f"Social Credit - {member.display_name}", value=self.users[member_id]['Social Credit'], inline=False)
            elif self.users[member_id]['Social Credit'] == 0:
                embed = discord.Embed(
                    color = discord.Color.light_grey()
                )
                embed.set_author(name=member.display_name, icon_url=ctx.author.avatar_url)
                embed.add_field(name=f"UwUs - {member.display_name}", value=self.users[member_id]['UwUs'], inline = False)
                embed.add_field(name=f"Social Credit - {member.display_name}", value=self.users[member_id]['Social Credit'], inline = False)
            else:
                embed = discord.Embed(
                    color = discord.Color.red()
                )
                embed.set_author(name=member.display_name, icon_url=ctx.author.avatar_url)
                embed.add_field(name=f"UwUs - {member.display_name}", value=self.users[member_id]['UwUs'], inline = False)
                embed.add_field(name=f"Social Credit - {member.display_name}", value=self.users[member_id]['Social Credit'], inline = False)
                
            await ctx.channel.send(embed=embed)



def setup(bot):
    bot.add_cog(SocialCredit(bot))
