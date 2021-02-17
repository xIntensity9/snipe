import discord
from discord.ext import commands

class Help(commands.Cog, name='Help'):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='help', invoke_without_command=True)
    async def help(self, ctx, command=None):
        if not command:
            embed=discord.Embed(description="To get an in-depth description of each command, type `$help <command>`\nArguments that are wrapped with `[ ]` means that they are required.\n**Last Updated: 1/22/21**", color=0xfdfdfd)
            embed.set_author(name="Help")
            embed.add_field(name="Snipe Commands", value="`$multisnipe <amount>`\n`$usersnipe [user]`\n`$snipe <channel>`\n`$editsnipe <channel>`")
            embed.add_field(name="Utility Commands", value="`$delchannel [arg] <channel_id>`\n`$editchannel [arg] <channel_id>`")
            embed.add_field(name="Misc. Commands", value="`$links`\n`$stats`\n`$vote`")
        elif command == "snipe":
            embed=discord.Embed(description="`$snipe <channel>`", color=0xfdfdfd)
            embed.set_author(name="Aliases: $s, $sniper, $sniped")
            embed.add_field(name="About this command", value="`$snipe` is a utility command that retrieves the message the was deleted most recently. (Excluding Bot Messages)")
            embed.add_field(name="`<channel>`", value="This argument allows you to specify a desired channel to snipe in. It is not required; if not specified, it will snipe the current channel.")
        elif command == "multisnipe":
            embed=discord.Embed(description="`$multisnipe <amount>`", color=0xfdfdfd)
            embed.set_author(name="Aliases: $multi, $msnipe, $m")
            embed.add_field(name="About this command", value="`$multisnipe` is a utility command that retrieves multiple deleted messages. (Will not retrieve deleted bot messages.)")
            embed.add_field(name="`<amount>`", value="This argument allows you to specify a desired amount of messages you want to be retrieved. If there is no input, it will be automatically set to 1.")
        elif command == "editsnipe":
            embed=discord.Embed(description="`$editsnipe <channel>`", color=0xfdfdfd)
            embed.set_author(name="Aliases: $esnipe, $edit, $e")
            embed.add_field(name="About this command", value="`$editsnipe` is a utility command that retrieves the message the was edited most recently. (Will not retrieve edited bot messages.)")
            embed.add_field(name="`<channel>`", value="This argument allows you to specify a desired channel to editsnipe in. It is not required; if not specified, it will editsnipe the current channel.")
        elif command == "usersnipe":
            embed=discord.Embed(description="`$usersnipe [user]`", color=0xfdfdfd)
            embed.set_author(name="Aliases: $usnipe, $snipeuser, $u")
            embed.add_field(name="About this command", value="`$usersnipe` is a utility command that retrieves the most recent deleted message from the targeted user. (Will not retrieve edited bot messages.)")
            embed.add_field(name="`[user]`", value="This argument selects what user to snipe, you must input a targeted user (@user or User#1234) to use this command.")
        elif command == "delchannel":
            embed=discord.Embed(description="`$delchannel [arg] <channel_id>`", color=0xfdfdfd)
            embed.set_author(name="Help for $delchannel")
            embed.add_field(name="About this command", value="`$delchannel` is a utility command that sets a certain channel to log all deleted messages (Excluding bot messages) in the server.")
            embed.add_field(name="`[arg]`", value="In this argument, you must specify what action you want to execute.\n`-a` is to add a new channel\n`-s` is to stop the logging\n`-u` is to update the existing channel")
            embed.add_field(name="`<channel_id>`", value="This argument is required for `-a` and `-u`, you must input the id of the channel you would like to display the messages in.")
            embed.add_field(name="Examples", value="`$delchannel -a 802551497891905557` - Add a delchannel\n`$delchannel -s` - Remove the delchannel\n`$delchannel -u 802551497891905557` - Update the current delchannel", inline=False)
        elif command == "editchannel":
            embed=discord.Embed(description="`$editchannel [arg] <channel_id>`", color=0xfdfdfd)
            embed.add_field(name="About this command", value="`$editchannel` is a utility command that sets a certain channel to log all edited messages (Excluding bot messages) in the server.")
            embed.add_field(name="`[arg]`", value="In this argument, you must specify what action you want to execute.\n`-a` is to add a new channel\n`-s` is to stop the logging\n`-u` is to update the existing channel")
            embed.add_field(name="`<channel_id>`", value="This argument is required for `-a` and `-u`, you must input the id of the channel you would like to display the messages in.")
            embed.add_field(name="Examples", value="`$editchannel -a 802551497891905557` - Add an editchannel\n`$editchannel -s` - Remove the editchannel\n`$editchannel -u 802551497891905557` - Update the current editchannel", inline=False)
        elif command == "links":
            embed=discord.Embed(description="`$links`", color=0xfdfdfd)
            embed.set_author(name="Help for $links")
            embed.add_field(name="About this command", value="`$links` is a misc. command that provides links related to Sniper. Currently, there are only invite links, and the top.gg page for Sniper. A GitHub page will be added in the future.")
        elif command == "stats":
            embed=discord.Embed(description="`$stats`", color=0xfdfdfd)
            embed.set_author(name="Help for $stats")
            embed.add_field(name="About this command", value="`$stats` is a misc. command that provides current stats for Sniper.")
        elif command == "vote":
            embed=discord.Embed(description="`$vote`", color=0xfdfdfd)
            embed.set_author(name="Help for $vote")
            embed.add_field(name="About this command", value="`$vote` is a misc. command that provides the link to vote for Sniper on Top.gg. If you voted, thanks! Your vote helps Sniper get better recognized by the community.")
        else:
            embed=discord.Embed(description="Invalid Command", color=0xfdfdfd)
            embed.set_author(name="Error", icon_url="https://cdn.discordapp.com/attachments/642491399790395397/743516486005424268/clipart1203855.png")
            embed.add_field(name="What happened?", value=f"`{command}` isn't a valid command.")
        try:
            await ctx.send(embed=embed)
        except NameError:
            ...

def setup(bot):
    bot.add_cog(Help(bot))
    print("Help has been loaded.")
