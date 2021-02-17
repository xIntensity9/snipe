import dbl
import discord
from discord.ext import commands

class topAPI(commands.Cog, name="topAPI"):

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc0Mjc4NDc2MzIwNjgyODAzMiIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA2MjM2MTkxfQ.7KeZ-yiX3v5eTY0HhM6jhtAwhayMpXD3c3_236FBT4I' # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True)

def setup(bot):
    bot.add_cog(topAPI(bot))
    print("topAPI has been loaded.")