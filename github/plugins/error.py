import discord
from discord.ext import commands
import datetime

class Error(commands.Cog, name='error'):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error_png = "https://cdn.discordapp.com/attachments/642491399790395397/743516486005424268/clipart1203855.png"
        try:
            if hasattr(ctx.command, 'on_error'):
                return
            else:
                embed=discord.Embed(description=f"`{ctx.command.qualified_name} {ctx.command.signature}`", color=0xfdfdfd)
                embed.set_author(name="Error", icon_url=error_png)
                embed.add_field(name="What happened?", value=f"{error}\n\nConstantly seeing this message and don't know what's wrong? Report it [here](https://top.gg/bot/742784763206828032).")
                await ctx.send(embed=embed)
        except:
            embed=discord.Embed(description=f"Undocumented Error", color=0xfdfdfd)
            embed.set_author(name="Error", icon_url=error_png)
            embed.add_field(name="What happened?", value=f"{error}\nConstantly seeing this message and don't know what's wrong? Report it [here](https://top.gg/bot/742784763206828032).")
            await ctx.send(embed=embed)

def setup(bot):
    print("Error has been loaded.")
    bot.add_cog(Error(bot))
