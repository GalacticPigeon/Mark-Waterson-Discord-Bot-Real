import discord
from discord.ext import commands

import random
import asyncio
import math

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
    
        self.deck_list = {
        "2♣": 2,   "2♦":  2,  "2♥":  2,  "2♠": 2,
        "3♣": 3,   "3♦":  3,  "3♥":  3,  "3♠": 3,
        "4♣": 4,   "4♦":  4,  "4♥":  4,  "4♠": 4,
        "5♣": 5,   "5♦":  5,  "5♥":  5,  "5♠": 5,
        "6♣": 6,   "6♦":  6,  "6♥":  6,  "6♠": 6,
        "7♣": 7,   "7♦":  7,  "7♥":  7,  "7♠": 7,
        "8♣": 8,   "8♦":  8,  "8♥":  8,  "8♠": 8,
        "9♣": 9,   "9♦":  9,  "9♥":  9,  "9♠": 9,
        "10♣": 10, "10♦": 10, "10♥": 10, "10♠": 10,
        "J♣": 10,  "J♦":  10, "J♥":  10, "J♠": 10,
        "Q♣": 10,  "Q♦":  10, "Q♥":  10, "Q♠": 10,
        "K♣": 10,  "K♦":  10, "K♥":  10, "K♠": 10,
        "A♣": 11,  "A♦":  11, "A♥":  11, "A♠": 11,
        }

        self.HIT = "\U0001F1ED"
        self.STAND = "\U0001F1F8"
        self.DELAY = 0.2
    
    # @commmands.command(aliases=['rr'])
    # async def russianroulette(self, ctx, bet_amount: str, bullet_count: int):
    #     return

    @commands.command(aliases=['uwus'])
    async def credit(self, ctx, member: discord.Member = None):
        """Checks a user's Social Credit and UwUs usage: `_credit` or `_credit [member]`"""
        member = ctx.author if not member else member
        member_id = str(member.id)
        guild_id = str(ctx.guild.id)

        user = await self.bot.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", member_id, guild_id)

        #If user is mark
        if member.id == 697112219162247179:
            embed = discord.Embed(
            color = discord.Color.magenta()
            )
            embed.set_author(name=member.display_name, icon_url=member.avatar_url)
            embed.add_field(name=f"UwUs - {member.display_name}", value="infinite", inline = False)
            embed.add_field(name=f"Social Credit - {member.display_name}", value="beyond human comprehension", inline = False)
            await ctx.channel.send(embed=embed)
        #If user is not in database
        elif not user:
            embed = discord.Embed(
                color = discord.Color.light_grey()
            )
            embed.set_author(name=member.display_name, icon_url=member.avatar_url)
            embed.add_field(name=f'Social Credit - {member.display_name}', value="No Social Credit", inline = False)
            await ctx.channel.send(embed=embed)
        else:
            #If user has positive sc
            if user[0]['sc'] > 0:
                embed = discord.Embed(
                    color = discord.Color.gold()
                )
                embed.set_author(name=member.display_name, icon_url=member.avatar_url)
                embed.add_field(name=f"UwUs - {member.display_name}", value=user[0]['uwus'], inline=False)
                embed.add_field(name=f"Social Credit - {member.display_name}", value=user[0]['sc'], inline=False)
            #If user has social credit
            elif user[0]['sc'] == 0:
                embed = discord.Embed(
                    color = discord.Color.light_grey()
                )
                embed.set_author(name=member.display_name, icon_url=member.avatar_url)
                embed.add_field(name=f"UwUs - {member.display_name}", value=user[0]['uwus'], inline = False)
                embed.add_field(name=f"Social Credit - {member.display_name}", value=user[0]['sc'], inline = False)
            #Every other case
            else:
                embed = discord.Embed(
                    color = discord.Color.red()
                )
                embed.set_author(name=member.display_name, icon_url=member.avatar_url)
                embed.add_field(name=f"UwUs - {member.display_name}", value=user[0]['uwus'], inline = False)
                embed.add_field(name=f"Social Credit - {member.display_name}", value=user[0]['sc'], inline = False)
                
            await ctx.channel.send(embed=embed)
    
    winCount = 0
    @commands.command(aliases=['toss', 'ct', 'flip'])
    async def cointoss(self, ctx, heads_or_tails: str = None, bet_amount: str = None):
        """Toss a coin and make a bet! You could win big! usage: `_cointoss [heads or tails] [amount]`"""
        author_id = str(ctx.author.id) 
        guild_id = str(ctx.guild.id)
        result = random.randint(1, 2)
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
            await ctx.send("How tf am I supposed to bet that? Enter a positive whole number")
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
        msg = await ctx.send("*Tossing coin...*") #Add animation here later?
        await asyncio.sleep(1)

        bet_amount = abs(bet_amount)
        if result == 2 and heads_or_tails == 'heads':
            await msg.edit(content=f"They won **{bet_amount * 2}** UwU(s)!")
            await self.bot.pg_con.execute("UPDATE users SET uwus = $1 WHERE user_id = $2 AND guild_id = $3", user[0]['uwus'] + bet_amount, author_id, guild_id)
        elif result == 1 and heads_or_tails == 'tails':
            await msg.edit(content=f"They won **{bet_amount * 2}** UwU(s)!")
            await self.bot.pg_con.execute("UPDATE users SET uwus = $1 WHERE user_id = $2 AND guild_id = $3", user[0]['uwus'] + bet_amount, author_id, guild_id)
        else:
            bet_amount = bet_amount * -1
            await msg.edit(content=f"They lost **{abs(bet_amount)}** UwU(s)!")
            await self.bot.pg_con.execute("UPDATE users SET uwus = $1 WHERE user_id = $2 AND guild_id = $3", user[0]['uwus'] + bet_amount, author_id, guild_id)

    
        
    @cointoss.error
    async def cointoss_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            time = "{:.2f}".format(error.retry_after)
            time = float(time)
            msg = 'Holy shit slow down, try again in {:.2f}s'.format(error.retry_after)
            await ctx.send(msg, delete_after=time)
        else:
            raise error
    
    
    @commands.command(aliases=['donate', 'send', 'gift'])
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
        if amount > user[0]['uwus']:
            await ctx.send(f"You can't send more than you have")
        
        if(member.bot):
            await ctx.send("You can't send UwUs to bots fuckass")
            return

        if (member_id == author_id):
            await ctx.send(f"**{ctx.author.display_name}** just sent ***__{amount}__*** UwU(s) to **{member.display_name}**! How kind and generous! They must be proud!")
        else:
            #Take UwUs from user
            await self.bot.pg_con.execute("UPDATE users SET uwus = $1 WHERE user_id = $2 AND guild_id = $3", user[0]['uwus'] - amount, author_id, guild_id)
            #Add UwUs to member
            user = await self.bot.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", member_id, guild_id)
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
            amount = random.randint(150, 600)
        
        await self.bot.pg_con.execute("UPDATE users SET uwus = $1 WHERE user_id = $2 AND guild_id = $3", 
        user[0]['uwus'] + amount, author_id, guild_id)
        await ctx.send(f"**{ctx.author.display_name}**, Here is your daily allowance of **{amount}** UwUs from ***__Mark Waterson__***")
    

    @commands.command(aliases=["lb"])
    async def leaderboard(self, ctx):
        """See who has the most Social Credit with this command! usage: `_leaderboard`"""
        guild_id = str(ctx.guild.id)
        limit = 5

        user = await self.bot.pg_con.fetch("SELECT user_id, guild_id, sc FROM users WHERE guild_id = $1 ORDER BY sc DESC LIMIT $2", guild_id, limit)
        print(f"\n{user}\n")
        leaders = []
        embed = discord.Embed(
            color = discord.Color.gold(),
        )
        member = await self.bot.fetch_user(user[0]["user_id"])
        embed.set_author(name=f"Top User: {member.display_name}", icon_url=member.avatar_url)
        for i in range(0,limit):
            person = user[i]["user_id"]
            person_credit = user[i]["sc"]
            try:
                member = await self.bot.fetch_user(person)
            except Exception as e:
                pass

            embed.add_field(name=f"Social Credit - {member.display_name}", value=user[i]['sc'], inline=False) 
        
        
        await ctx.channel.send(embed=embed)
    
    #BLACKJACK
    @commands.command(aliases=["bj"])
    @commands.bot_has_permissions(manage_emojis=True, manage_messages=True)
    async def blackjack(self, ctx, bet=None):
        """This is blackjack what did you expect
        usage: `_blackjack [amount]`"""
        bet = "1" if not bet else bet

        if not bet.isdigit():
            return await ctx.channel.send(
                f":x: A bet can only be a positive integer! Enter `_blackjack [bet]` and don't try to fuck the system next time!"
            )

        self.bet = int(bet)
        self.author_id = str(ctx.author.id)
        self.guild_id = str(ctx.guild.id)
        author_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)

        self.user = await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", 
        author_id, guild_id)

        if self.bet > self.user["uwus"]:
            return await ctx.channel.send(
                f":x: Not enough UwUs. Your balance is {self.user['uwus']} UwUs. Enter a smaller amount or `_daily` to get some UwUs"
            )

        await self.bot.pg_con.execute("UPDATE users SET uwus = $1 WHERE user_id = $2 AND guild_id = $3", self.user['uwus'] - self.bet, author_id, guild_id)

        self.player = []
        self.dealer = []

        self.deck = [card for card in self.deck_list]

        # Game setup
        self.setup_turn()
        self.embed = self.update_ui(ctx)
        self.stop_flag = False
        await self.check_blackjack(ctx)
        self.msg = await ctx.channel.send(embed=self.embed)
        await self.msg.edit(embed=self.embed)

        await self.msg.add_reaction(self.HIT)
        await self.msg.add_reaction(self.STAND)

        self.hit_clicked = False
        self.stand_clicked = False

        def check_reaction(reaction, user):
            if str(reaction.emoji) == self.HIT:
                self.hit_clicked = True
                return user == ctx.author and str(reaction.message) == str(self.msg)
            elif str(reaction.emoji) == self.STAND:
                self.stand_clicked = True
                return user == ctx.author and str(reaction.message) == str(self.msg)

        # Game loop
        while True:
            if self.stop_flag:
                break

            try:
                reaction = await self.bot.wait_for(
                    "reaction_add", check=check_reaction, timeout=60.0
                )
            except asyncio.TimeoutError:
                reaction = self.stand_clicked = True
                await ctx.channel.send(
                    f":x: {ctx.author.mention} you took too long, your game has been closed, to start over, enter `{_}blackjack` command"
                )
            if reaction and self.hit_clicked:
                self.hit_clicked = False

                self.get_card(self.player)
                self.embed = self.update_ui(ctx)
                await self.msg.edit(embed=self.embed)

                if self.check_edge(self.player):
                    color = False
                    self.embed = self.update_ui(ctx, "BUST", True, discord.Color.red())
                    await self.msg.edit(embed=self.embed)
                    break

                await self.msg.remove_reaction(self.HIT, ctx.author)

            elif reaction and self.stand_clicked:
                self.stand_clicked = False

                self.embed = self.update_ui(ctx, "Dealer's hand", True)
                await self.msg.edit(embed=self.embed)
                await asyncio.sleep(self.DELAY)

                while self.get_score(self.dealer) < 17:
                    self.get_card(self.dealer)
                    self.embed = self.update_ui(ctx, "Drawing...", True)
                    await self.msg.edit(embed=self.embed)
                    await asyncio.sleep(self.DELAY)

                if self.check_edge(self.dealer):
                    await self.bot.pg_con.execute("UPDATE users SET uwus = $1 WHERE user_id = $2 AND guild_id = $3", self.user['uwus'] + self.bet * 2, 
                    self.author_id, self.guild_id)
                    self.embed = self.update_ui(ctx, "WIN", True, discord.Color.green())
                    await self.msg.edit(embed=self.embed)
                    break
                
                result = await self.check_result()
                if result == "WIN":
                    if self.get_score(self.player) == 21:
                        color = discord.Color.default()
                        result = "YOU HAVE BLACKJACK\n YOU WIN"
                    else:
                        color = discord.Color.green()
                elif result == "PUSH":
                    color = discord.Color.greyple()
                else:
                    if self.get_score(self.dealer) == 21:
                        color = discord.Color.red()
                        result = "MARK HAS BLACKJACK\n YOU LOSE HAHA"
                    else:
                        color = discord.Color.red()
                
                self.embed = self.update_ui(ctx, result, True, color)
                await self.msg.edit(embed=self.embed)
                break

    def get_card(self, user):
        card = random.choice(self.deck)
        user.append(card)
        self.deck.remove(card)
        return card

    def get_score(self, user, ra9=True):
        if not ra9:
            return str(self.deck_list.get(user[0]))

        deck_score = []
        for n in user:
            deck_score.append(self.deck_list.get(n))

        if sum(deck_score) > 21:
            for i, n in enumerate(deck_score):
                if deck_score[i] == 11:
                    deck_score[i] = 1

        return sum(deck_score)

    def show_cards(self, user, ra9=True):
        if ra9:
            return " ".join("`" + item + "`" for item in user)
        return "`" + user[0] + "` `?`"

    def update_ui(self, ctx_m, footer_m="Would you like\nto stand on it?", ra9=False, color=None):
        color = ctx_m.author.color if not color else color
        embed = discord.Embed(color=color)
        embed.set_author(name="Blackjack", icon_url=ctx_m.author.avatar_url)
        embed.set_footer(text=footer_m, icon_url=self.bot.user.avatar_url)
        embed.add_field(
            name=f"Your score: **{self.get_score(self.player)}**",
            value=self.show_cards(self.player),
            inline=False,
        )
        embed.add_field(
            name=f"Dealer score: **{self.get_score(self.dealer, ra9)}**",
            value=self.show_cards(self.dealer, ra9),
            inline=False,
        )
        return embed

    def setup_turn(self):
        self.get_card(self.player)
        self.get_card(self.dealer)
        self.get_card(self.player)
        self.get_card(self.dealer)

    def check_edge(self, user):
        if self.get_score(user) > 21:
            return True
        return False

    async def check_result(self):
        if (
            self.get_score(self.player) > self.get_score(self.dealer)
        ) and not self.check_edge(self.player):
            await self.bot.pg_con.execute("UPDATE users SET uwus = $1 WHERE user_id = $2 AND guild_id = $3", self.user['uwus'] + self.bet, 
            self.author_id, self.guild_id)
            return "WIN"
        elif self.get_score(self.player) == self.get_score(self.dealer):
            await self.bot.pg_con.execute("UPDATE users SET uwus = $1 WHERE user_id = $2 AND guild_id = $3", self.user['uwus'], 
            self.author_id, self.guild_id)
            return "PUSH"
        else:
            return "LOSE"

    async def check_blackjack(self, ctx_m):
        if self.get_score(self.player, True) == 21:
            if self.get_score(self.dealer, True) == 21:
                await self.bot.pg_con.execute("UPDATE users SET uwus = $1 WHERE user_id = $2 AND guild_id = $3", self.user['uwus'], author_id, guild_id)
                color = discord.Color.greyple()
                self.embed = self.update_ui(ctx_m, "BLACKJACK\n PUSH", True, color)
                self.stop_flag = True
            else:
                await self.bot.pg_con.execute("UPDATE users SET uwus = $1 WHERE user_id = $2 AND guild_id = $3", self.user['uwus'] + self.bet * 2, 
                self.author_id, self.guild_id)
                color = discord.Color.default();
                self.embed = self.update_ui(ctx_m, "YOU HAVE BLACKJACK\n YOU WIN", True, color)
                self.stop_flag = True
        elif self.get_score(self.dealer, True) == 21:
            color = discord.Color.red()
            self.embed = self.update_ui(ctx_m, "MARK HAS BLACKJACK\n YOU LOSE HAHA", True, color)
            self.stop_flag = True
    
    @blackjack.error
    async def blackjack_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            time = "{:.2f}".format(error.retry_after)
            time = float(time)
            msg = 'Holy shit slow down, try again in {:.2f}s'.format(error.retry_after)
            await ctx.send(msg, delete_after=time)
        elif isinstance(error, commands.BotMissingPermissions):
            msg = ":x: {:}".format(error)
            await ctx.send(msg, delete_after=3)
        else:
            raise error

    #STEAL COMMAND (EVIL)
    # @commands.command()
    # @commands.bot_has_permissions(manage_messages=True)
    # @commands.cooldown(1, 86,400, commands.BucketType.user)
    # async def steal(self, ctx, member: Discord.Member = None):
    #     """STEAL UWUs FROM OTHER PEOPLE (EVIL)"""
    #     if not member:
    #         await ctx.send("Steal from yourself??? Tf???")
    #         return
    #     elif member.bot:
    #         await ctx.send("Bots do not participate in your economy")
    #         return
    #     max_uwus = 50000 #Maximum number that the user can steal
    #     author_id = str(ctx.author.id) 
    #     guild_id = str(ctx.guild.id)
    #     member_id = str(member.id)

    #     #Check if user is trying to steal more than the target has or more uwus than allowed
    #     user = await self.bot.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", member_id, guild_id)

        
    #     #Stop the steal if user has less than lowerlimit UwUs or
    #     lowerlimit = 3000
    #     if user[0]['uwus'] < lowerlimit:
    #         await ctx.send(f"{ctx.member.display_name} has less than {lowerlimit} UwUs and is immune to theft")
    #         return
        
    #     #Chance that a steal is successful
    #     steal = random.randint(0,10)
    #     #percent to be stolen
    #     percentage = math.ceil(100.0 * random.uniform(0.01, 0.05)) / 100.0
    #     #Lower the chance if target blocks the steal
    #     Events = self.bot.get_cog("Events")
    #     steal = random.randint(0, Events.isBlock())

        



    #     await ctx.send(f"{ctx.author.display_name} has attempted to steal {steal} UwUs from {ctx.member.display_name}! Reply with `_block` to block the steal!")




        
        



def setup(bot):
    bot.add_cog(Gambling(bot))
