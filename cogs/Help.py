import discord
from discord.ext import commands    

excludeList = ['SocialCredit', 'Help']

class Help(commands.Cog):
    """This only contains the help command."""
    def __init__(self, bot):
        self.bot = bot
    
    def caseInsensitively(self, thing1, thing2):
        same = False
        temp1 = thing1
        temp2 = thing2
        if str(temp1).lower() == str(temp2).lower():
            same = True
        return same

    @commands.command()
    @commands.has_permissions(add_reactions=True,embed_links=True)
    async def help(self,ctx,*cog):
        """Gets all cogs and commands."""
        try:
            if not cog:
                halp=discord.Embed(title='Cog Listing and Uncatergorized Commands',
                                description='Use `_help *cog*` to find out more about them!')
                cogs_desc = ''
                for x in self.bot.cogs:
                    if x not in excludeList:
                        cogs_desc += ('{} - {}'.format(x,self.bot.cogs[x].__doc__)+'\n')
                
                halp.add_field(name='Cogs',value=cogs_desc[0:len(cogs_desc)-1],inline=False)
                cmds_desc = ''
                for y in self.bot.walk_commands():
                    if not y.cog_name and not y.hidden:
                        cmds_desc += ('{} - {}'.format(y.name,y.help)+'\n')
                halp.add_field(name='Uncatergorized Commands',value=cmds_desc[0:len(cmds_desc)-1],inline=False)
                await ctx.send('',embed=halp)
            else:
                if len(cog) > 1:
                    halp = discord.Embed(title='Error!',description='That is way too many cogs!',color=discord.Color.red())
                    await ctx.send('',embed=halp)
                else:
                    found = False
                    for x in self.bot.cogs:
                        for y in cog:
                            if self.caseInsensitively(x,y):
                                y = x
                                halp=discord.Embed(title=cog[0]+' Command Listing',description=self.bot.cogs[y].__doc__)
                                for c in self.bot.get_cog(y).get_commands():
                                    if not c.hidden:
                                        halp.add_field(name=c.name,value=c.help,inline=False)
                                found = True
                    if not found:
                        halp = discord.Embed(title='Error!',description='That is not a cog fuckass',color=discord.Color.red())
                    await ctx.send('',embed=halp)
        except Exception as e:
            raise e
            pass

def setup(bot):
    bot.add_cog(Help(bot))