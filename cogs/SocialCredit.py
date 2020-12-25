import discord
from discord.ext import commands

import random

def remove_symbol(message):
    #list of chars to remove
    badCharsList = [';', ' ', '.', "'", '"', '!', '*', '_', '#', '~', '(', ')', '|', '{', '}', 
    '<', '>', '?', "\\", '/', '-', '+', '=', '^', '$', '&', '%' ',', '`', "’"]

class SocialCredit(commands.Cog):
    """Commands dealing with Social Credit and UwUs!"""
    def __init__(self, bot):
        self.bot = bot

    async def remove_points(self, author_id: str, guild_id: str, count, message):
        user = await self.bot.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)
        num_uwus = user[0]['uwus']
        if num_uwus <= 0:
            return
        if count > num_uwus:
            count = num_uwus
        user = await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)
        await self.bot.pg_con.execute("UPDATE users SET uwus = $1 WHERE user_id = $2 AND guild_id = $3", user['uwus'] - count, author_id, guild_id)
    
    async def change_lvl(self, user):
        curr_uwus = user['uwus']
        curr_social_credit = user['sc']
        gain_function = round(2.1003*(curr_social_credit ** 3)- 0.0025*(curr_social_credit ** 2) + 15.454 * (curr_social_credit) + 0.7534)
        remove_function = round(2.1003*((curr_social_credit - 1) ** 3)- 0.0025*((curr_social_credit - 1) ** 2) + 15.454 * (curr_social_credit - 1) + 0.7534)
        count = 0

        if curr_uwus >= gain_function:
            while curr_uwus >= gain_function:
                count = count + 1
                gain_function = round(2.1003*((curr_social_credit + count) ** 3)- 0.0025*((curr_social_credit + count) ** 2) + 15.454 * (curr_social_credit + count) + 0.7534)

            await self.bot.pg_con.execute("UPDATE users SET sc = $1 WHERE user_id = $2 AND guild_id = $3", curr_social_credit + count, user['user_id'], user['guild_id'])
            return count
        elif curr_uwus < (remove_function - 17):
            while curr_uwus < (remove_function - 17):
                count = count + 1
                remove_function = round(2.1003*((curr_social_credit - count) ** 3)- 0.0025*((curr_social_credit - count) ** 2) + 15.454 * (curr_social_credit - count) + 0.7534)

            curr_social_credit = curr_social_credit - count
            await self.bot.pg_con.execute("UPDATE users SET sc = $1 WHERE user_id = $2 AND guild_id = $3", curr_social_credit, user['user_id'], user['guild_id'])
            count = count * -1
            return count
        else:
            return -1

    @commands.Cog.listener()
    async def on_member_join(self, member):
        user_id = str(member.id)
        guild_id = str(member.guild.id)

        user = await self.bot.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", user_id, guild_id)
        
        if not user:
            await self.bot.pg_con.execute("INSERT INTO users (user_id, guild_id, uwus, sc) VALUES ($1, $2, 10, 1)", user_id, guild_id)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.id == 697112219162247179:
            return

        author_id = str(message.author.id)
        guild_id = str(message.guild.id)

        user = await self.bot.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)
        
        if not user:
            await self.bot.pg_con.execute("INSERT INTO users (user_id, guild_id, uwus, sc) VALUES ($1, $2, 10, 1)", author_id, guild_id)

        def reward_uwus():
            num = random.randint(0,70)

            if num == 0:
                return True
            else:
                return False
        
        user = await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)
        if reward_uwus():
            num_uwus = random.randint(-15,50)
            await self.bot.pg_con.execute("UPDATE users SET uwus = $1 WHERE user_id = $2 AND guild_id = $3", user['uwus'] + num_uwus, author_id, guild_id)
            if num_uwus >= 0:
                embed = discord.Embed(
                    color = discord.Color.green()
                )
                embed.set_author(name='halal')
                embed.add_field(name=f"\u200b", value=f"You have gained {num_uwus} UwU(s)", inline=False)
            else:
                embed = discord.Embed(
                    color = discord.Color.red()
                )
                embed.set_author(name='haram')
                embed.add_field(name=f"\u200b", value=f"You have lost {abs(num_uwus)} UwU(s)", inline=False)
            
            await message.channel.send(embed=embed)


        if not "_reset" in message.content.lower():
            num = await self.change_lvl(user)
            if await self.change_lvl(user) > 0:
                if num > 1:
                    embed = discord.Embed(
                        color = discord.Color.orange()
                    )
                    embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
                    embed.add_field(name='\u200b', value=f"{message.author.display_name} now has a Social Credit of {user['sc'] + num}", inline = False)
                    await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(
                        color = discord.Color.orange()
                    )
                    embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
                    embed.add_field(name='\u200b', value=f"{message.author.display_name} now has a Social Credit of {user['sc'] + 1}", inline = False)
                    await message.channel.send(embed=embed)
    

    #Resets entered user's points
    @commands.command(hidden=True)
    @commands.is_owner()
    async def reset(self, ctx, member: discord.Member = None):
        """Owner only command do not concern yourself mortal"""
        member = ctx.author if not member else member
        member_id = str(member.id)
        guild_id = str(ctx.guild.id)

        #FIXME: DELETE?
        #user = await self.bot.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", member_id, guild_id)

        try:
            await self.bot.pg_con.execute("UPDATE users SET uwus = $1 WHERE user_id = $2 AND guild_id = $3", 10, member_id, guild_id)
            await self.bot.pg_con.execute("UPDATE users SET sc = $1 WHERE user_id = $2 AND guild_id = $3", 1, member_id, guild_id)
            await ctx.channel.send(f"{member.display_name}'s Social Credit and UwUs have been reset")
        except Exception as e:
            raise e
            pass

    #Lets me add uwus for testing
    @commands.command(hidden=True)
    @commands.is_owner()
    async def add(self, ctx, num, member: discord.Member = None):
        """Owner only command do not concern yourself mortal"""
        member = ctx.author if not member else member
        member_id = str(member.id)
        guild_id = str(ctx.guild.id)

        user = await self.bot.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", member_id, guild_id)

        try: 
            await self.bot.pg_con.execute("UPDATE users SET uwus = $1 WHERE user_id = $2 AND guild_id = $3", user[0]['uwus'] + int(num), member_id, guild_id)
        except Exception as e:
            raise e
            pass



def setup(bot):
    bot.add_cog(SocialCredit(bot))
