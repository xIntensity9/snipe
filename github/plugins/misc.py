import discord
from discord.ext import commands
import sqlite3
from Bot import error_embed
import math
import time

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)

startTime = time.time()

def getUptime():
    return time.time() - startTime

class Misc(commands.Cog, name='Misc'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def links(self, ctx):
        embed=discord.Embed(description="Links for Sniper", color=0xfdfdfd)
        embed.set_author(name="Links")
        embed.add_field(name="Invite Links", value="[Manage Messages](https://discord.com/api/oauth2/authorize?client_id=742784763206828032&permissions=8192&scope=bot)\n[Administrator](https://discord.com/api/oauth2/authorize?client_id=742784763206828032&permissions=8&scope=bot)")
        embed.add_field(name="Notice", value="You need the permission `Manage Server` to invite bots to your server!")
        embed.add_field(name="Misc.", value="[Top.gg](https://top.gg/bot/742784763206828032)", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def vote(self, ctx):
        embed=discord.Embed(description="Thanks for voting! Your vote helps Sniper get better recognized by the community!", color=0xfdfdfd)
        embed.set_author(name="Vote")
        embed.add_field(name="Direct Link", value="https://top.gg/bot/742784763206828032/vote")
        await ctx.send(embed=embed)

    @commands.command()
    async def stats(self, ctx):
        try:
            c = sqlite3.connect("files/stats.db")
            cursor = c.cursor()
            
            embed=discord.Embed(description=f"Current Stats for Sniper", color=0xfdfdfd)
            embed.set_author(name=f"Stats")

            embed.add_field(name=f"Total Server Count: `{len(self.bot.guilds)}`", value=f"Current server count for Sniper")
            #embed.add_field(name=f"Total Users: `{len(set(self.bot.get_all_members()))}`", value=f"Total users for Sniper.", inline=False) # Fix Total Users
            embed.add_field(name=f"Uptime: `{convert(getUptime())}`", value=f"Current uptime for Sniper (hh:mm:ss)", inline=False)
            embed.add_field(name=f"Library: `Discord.py (DPY)`", value=f"Library used for Sniper", inline=False)
            embed.add_field(name=f"Developer: `xIntensity#4818`", value=f"Developer of Sniper",)

            

            # idea, add global stats as value

            # Local Stats
            """
            cursor.execute(f"SELECT snipe FROM stats WHERE guild_id={ctx.guild.id}")
            embed.add_field(name=f"Messages Sniped: {cursor.fetchone()[0]}", value=f"Total amount of messages sniped", inline=False)
            cursor.execute(f"SELECT esnipe FROM stats WHERE guild_id={ctx.guild.id}")
            embed.add_field(name=f"Messages Editsniped: {cursor.fetchone()[0]}", value=f"Total amount of edited messages sniped", inline=False)
            cursor.execute(f"SELECT delmsg FROM stats WHERE guild_id={ctx.guild.id}")
            embed.add_field(name=f"Deleted Messages Logged: {cursor.fetchone()[0]}", value=f"Total amount of deleted messages logged", inline=False)
            cursor.execute(f"SELECT editmsg FROM stats WHERE guild_id={ctx.guild.id}")
            embed.add_field(name=f"Edited Messages Logged: {cursor.fetchone()[0]}", value=f"Total amount of edited messages logged", inline=False)
            embed.set_footer(text=f"Server ID: {ctx.guild.id}", icon_url=ctx.guild.icon_url)
            """

            # Global Stats
            """     
            cursor.execute(f"SELECT snipe FROM stats WHERE guild_id={int(-1)}")
            embed.add_field(name="Messages Sniped", value=f"`{cursor.fetchone()[0]}`")
            cursor.execute(f"SELECT esnipe FROM stats WHERE guild_id={int(-1)}")
            embed.add_field(name="Messages Editsniped", value=f"`{cursor.fetchone()[0]}`")
            cursor.execute(f"SELECT delmsg FROM stats WHERE guild_id={int(-1)}")
            embed.add_field(name="Deleted Messages Logged", value=f"`{cursor.fetchone()[0]}`")
            cursor.execute(f"SELECT editmsg FROM stats WHERE guild_id={int(-1)}")
            embed.add_field(name="Edited Messages Logged", value=f"`{cursor.fetchone()[0]}`")
            """

            await ctx.send(embed=embed)

        except TypeError:
            await ctx.send(embed=error_embed("Stat Database Error","This server's database is misconfigurated. Try this command again."))
            connect = sqlite3.connect("files/stats.db")
            cursor = connect.cursor()

            cursor.execute(f"INSERT into stats VALUES ({ctx.guild.id}, 0, 0, 0, 0)")

            connect.commit()
            connect.close()


def setup(bot):
    bot.add_cog(Misc(bot))
    print("Misc has been loaded.")