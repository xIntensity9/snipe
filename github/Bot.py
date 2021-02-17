import discord
import json
from discord.ext import commands
import sys
import sqlite3
import datetime
import traceback

client = commands.Bot(command_prefix="$") # CHANGE BACK TO $

def error_embed(description, error):
    embed=discord.Embed(description=description, color=0xfdfdfd)
    embed.set_author(name="Error", icon_url="https://cdn.discordapp.com/attachments/642491399790395397/743516486005424268/clipart1203855.png")
    embed.add_field(name="What happened?", value=error)
    return embed

def success_embed(description, completed):
    embed=discord.Embed(description=description, color=0xfdfdfd)
    embed.set_author(name="Success", icon_url="https://cdn.discordapp.com/attachments/742833913751142402/743524321376338051/pngwing.com.png")
    embed.add_field(name="Action Completed:", value=completed)
    return embed

@client.event
async def on_ready():
    
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"$snipe | $help"))

    cogs = ['plugins.snipe', 'plugins.help','plugins.misc','plugins.error','plugins.topAPI']

    for cog in cogs:
        try:
            client.load_extension(cog)
        except Exception:
            print(f'Cant load {cog}', file=sys.stderr)
            traceback.print_exc()

    print("Bot has connected.")

client.help_command = None

"""
@client.event
async def on_guild_join(guild):
    connect = sqlite3.connect("files/stats.db")
    cursor = connect.cursor()

    cursor.execute(f"INSERT into stats VALUES ({guild.id}, 0, 0, 0, 0)")

    connect.commit()
    connect.close()
""" # enable stats

@client.event
async def on_guild_remove(guild):

    # Clear out all options for the server

    c = sqlite3.connect("files/edit_log.db")
    cursor = c.cursor()
    cursor.execute(f"SELECT * FROM servers WHERE guild_id={guild.id}")
    if not cursor.fetchone():
        ...
    else:
        cursor.execute(f"DELETE from servers WHERE guild_id='{guild.id}'")
    c.commit()
    c.close()

    c = sqlite3.connect("files/message_log.db")
    cursor = c.cursor()
    cursor.execute(f"SELECT * FROM servers WHERE guild_id={guild.id}")
    if not cursor.fetchone():
        ...
    else:
        cursor.execute(f"DELETE from servers WHERE guild_id='{guild.id}'")
    c.commit()
    c.close()

    """
    c = sqlite3.connect("files/stats.db")
    cursor = c.cursor()
    cursor.execute(f"SELECT * FROM stats WHERE guild_id={guild.id}")
    if not cursor.fetchone():
        ...
    else:
        cursor.execute(f"DELETE from stats WHERE guild_id='{guild.id}'")
    c.commit()
    c.close()
    """ # enable stats

@client.event
async def on_message_edit(before, after):
    if before.author.bot is False:
        if len(before.content) == 0 and len(after.content) == 0: # Filter out other events
            ...
        else:
            connect = sqlite3.connect("files/edit_log.db")

            cursor = connect.cursor()

            cursor.execute(f"SELECT * FROM servers WHERE guild_id={after.guild.id}")
            if not cursor.fetchone():
                ...
            else:
                cursor.execute(f"SELECT channel_id FROM servers WHERE guild_id={after.guild.id}")
                
                channel = client.get_channel(cursor.fetchone()[0])
                c = client.get_channel(before.channel.id)
                embed=discord.Embed(description=f"A message was edited in {c.mention}", color=0xfdfdfd)
                embed.set_author(name="Edited Message", icon_url=before.author.avatar_url)
                embed.add_field(name="Before", value=before.content)
                embed.add_field(name="After", value=after.content)
                embed.add_field(name="Message ID", value=f"`{after.id}`", inline=False)
                embed.add_field(name="Author", value=before.author)
                await channel.send(embed=embed)

                """
                c = sqlite3.connect("files/stats.db")
                cursor = c.cursor()

                cursor.execute(f"SELECT editmsg FROM stats WHERE guild_id={before.guild.id}")
                cursor.execute(f"UPDATE stats SET editmsg = {cursor.fetchone()[0] + 1} WHERE guild_id={before.guild.id}")

                c.commit()
                c.close()
                """

    else:
        ...

@client.event
async def on_message_delete(message):
    if message.author.bot is False:
        connect = sqlite3.connect("files/message_log.db")

        cursor = connect.cursor()

        cursor.execute(f"SELECT * FROM servers WHERE guild_id={message.guild.id}")
        if not cursor.fetchone():
            ...
        else:
            cursor.execute(f"SELECT channel_id FROM servers WHERE guild_id={message.guild.id}")
            
            channel = client.get_channel(cursor.fetchone()[0]) 
            c = client.get_channel(message.channel.id)
            embed=discord.Embed(description=f"A message was deleted in {c.mention}", color=0xfdfdfd)
            if len(message.content) == 0:
                embed.add_field(name = f"Message ", value=f"(No message was provided)")
            else:
                embed.add_field(name = f"Message ", value=f"{message.content}")
            embed.set_author(name="Deleted Message", icon_url=message.author.avatar_url)
            embed.add_field(name="Message ID", value=f"`{message.id}`", inline=False)
            embed.add_field(name="Author", value=message.author, inline=False)

            if message.attachments:
                embed.add_field(name='Attachment(s)', value='\n'.join([attachment.filename for attachment in message.attachments]) + "\n\n*Images and files __cannot__ be recovered after being deleted!*")
            await channel.send(embed=embed)

            """
            c = sqlite3.connect("files/stats.db")
            cursor = c.cursor()

            cursor.execute(f"SELECT delmsg FROM stats WHERE guild_id={message.guild.id}")
            cursor.execute(f"UPDATE stats SET delmsg = {cursor.fetchone()[0] + 1} WHERE guild_id={message.guild.id}")

            c.commit()
            c.close()
            """

    else:
        ...


@commands.has_permissions(manage_guild=True)
@client.command()
async def editchannel(ctx, arg=None, channel_id=None):

    connect = sqlite3.connect("files/edit_log.db")
    cursor = connect.cursor()

    if not arg:
        await ctx.send(embed=error_embed("`<argument>` not specified.", "Please specify what you wish to do with `$editchannel`\nTyping `$help editchannel` will give you a list of `$editchannel` usages."))
    
    else:
        if arg == "-u":
            cursor.execute(f"SELECT EXISTS(SELECT 1 FROM servers WHERE guild_id='{ctx.guild.id}')")

            if cursor.fetchone()[0] == 0:
                await ctx.send(embed=error_embed("This action could not be completed.", "Your server does not have a specified channel to log deleted messages!"))

            else:
                try:
                    c = client.get_channel(int(channel_id))
                    if c == None:
                        await ctx.send(embed=error_embed("Invalid channel ID", "The `<channel_id>` you have entered is not valid."))

                    else:
                        cursor.execute(f"SELECT channel_id FROM servers WHERE guild_id={ctx.guild.id}")
                        if cursor.fetchone()[0] == int(channel_id):

                            await ctx.send(embed=error_embed("Channel already logging.", "The channel ID you have enter is already being used as a edited-message logger."))

                        else:
                            if str(client.get_channel(int(channel_id)).guild) != str((client.get_guild(ctx.guild.id)).name):
                                await ctx.send(embed=error_embed(f"Invalid channel ID `({channel_id})`", "Please enter a channel ID __within__ the server.\nChannels from other servers cannot be used."))

                            else:
                                cursor.execute(f"UPDATE servers SET channel_id={channel_id} WHERE guild_id={ctx.guild.id}")
                                await ctx.send(embed=success_embed("Action has been completed successfully!", f"All edited messages in `{ctx.guild.name}` are logged in {client.get_channel(int(channel_id)).mention}"))
                                connect.commit()

                except ValueError:
                    await ctx.send(embed=error_embed("Incorrect data type","`<channel_id>` only accepts number data types! (You can't enter words)"))

        elif arg == "-s":
            cursor.execute(f"SELECT EXISTS(SELECT 1 FROM servers WHERE guild_id='{ctx.guild.id}')")

            if cursor.fetchone()[0] == 0:
                await ctx.send(embed=error_embed("This action could not be completed.", "Your server does not have a specified channel to log edited messages!"))

            else:
                cursor.execute(f"SELECT channel_id FROM servers WHERE guild_id={ctx.guild.id}")
                channel = client.get_channel(cursor.fetchone()[0])
                cursor.execute(f"DELETE from servers WHERE guild_id='{ctx.guild.id}'")
                connect.commit()
                server = client.get_guild(ctx.guild.id)
                await ctx.send(embed=success_embed("Action has been completed successfully!", f"Edited messages no longer logged for `{server}`\nEdited messages no longer yielded in {channel.mention}"))

        elif arg == "-a":
            cursor.execute(f"SELECT * FROM servers WHERE guild_id={ctx.guild.id}")

            if not cursor.fetchone():
                try:
                    c = client.get_channel(int(channel_id))
                    if c == None:
                        await ctx.send(embed=error_embed("Invalid channel ID","The `<channel_id>` you have entered is not valid."))
                        
                    else:
                        if str(client.get_channel(int(channel_id)).guild) != str((client.get_guild(ctx.guild.id)).name):
                            await ctx.send(embed=error_embed(f"Invalid channel ID `({channel_id})`","Please enter a channel ID __within__ the server.\nChannels from other servers cannot be used."))

                        else:
                            cursor.execute(f"INSERT INTO servers VALUES ({ctx.guild.id}, {channel_id})")
                            await ctx.send(embed=success_embed("Action has been completed successfully!",f"All edited messages in `{ctx.guild.name}` are logged in {client.get_channel(int(channel_id)).mention}"))
                            connect.commit()

                except ValueError:
                        await ctx.send(embed=error_embed("Incorrect data type.","`<channel_id>` only accepts number data types! (You can't enter words)"))

            else:
                cursor.execute(f"SELECT channel_id FROM servers WHERE guild_id={ctx.guild.id}")
                channel = client.get_channel(cursor.fetchone()[0])
                await ctx.send(embed=error_embed("Existing Logging Channel",f"{channel.mention} has already been set for the edited-message logger.\nYou can update it with `$editchannel -u <channel_id>`"))

            connect.close()



@commands.has_permissions(manage_guild=True)
@client.command()
async def delchannel(ctx, arg=None, channel_id=None):

    connect = sqlite3.connect("files/message_log.db")
    cursor = connect.cursor()

    if not arg:
        await ctx.send(embed=error_embed("`<argument>` not specified.","Please specify what you wish to do with `$delchannel`\nTyping `$help delchannel` will give you a list of `$delchannel` usages."))
    
    else:
        if arg == "-u":
            cursor.execute(f"SELECT EXISTS(SELECT 1 FROM servers WHERE guild_id='{ctx.guild.id}')")

            if cursor.fetchone()[0] == 0:
                await ctx.send(embed=error_embed("No specified channel!","Your server does not have a specified channel to log deleted messages!"))

            else:
                try:
                    c = client.get_channel(int(channel_id))
                    if c == None:
                        await ctx.send(embed=error_embed("Invalid channel ID","The `<channel_id>` you have entered is not valid"))
                    
                    else:
                        cursor.execute(f"SELECT channel_id FROM servers WHERE guild_id={ctx.guild.id}")
                        if cursor.fetchone()[0] == int(channel_id):
                            await ctx.send(embed=error_embed("Channel already logging.","The channel ID you have enter is already being used as a deleted-message logger."))
                        
                        else:
                            if str(client.get_channel(int(channel_id)).guild) != str((client.get_guild(ctx.guild.id)).name):
                                await ctx.send(embed=error_embed(f"Invalid channel ID `({channel_id})`", "Please enter a channel ID __within__ the server.\nChannels from other servers cannot be used."))

                            else:
                                cursor.execute(f"UPDATE servers SET channel_id={channel_id} WHERE guild_id={ctx.guild.id}")
                                await ctx.send(embed=success_embed("Action has been completed successfully!",f"All deleted messages in `{ctx.guild.name}` are logged in {client.get_channel(int(channel_id)).mention}"))
                                connect.commit()

                except ValueError:
                        await ctx.send(embed=error_embed("Incorrect data type.","`<channel_id>` only accepts number data types! (You can't enter words)"))

        elif arg == "-s":
            cursor.execute(f"SELECT EXISTS(SELECT 1 FROM servers WHERE guild_id='{ctx.guild.id}')")

            if cursor.fetchone()[0] == 0:
                await ctx.send(embed=error_embed("No specified channel!","Your server does not have a specified channel to log deleted messages!"))

            else:
                cursor.execute(f"SELECT channel_id FROM servers WHERE guild_id={ctx.guild.id}")
                channel = client.get_channel(cursor.fetchone()[0])
                cursor.execute(f"DELETE from servers WHERE guild_id='{ctx.guild.id}'")
                connect.commit()
                server = client.get_guild(ctx.guild.id)
                await ctx.send(embed=success_embed("Action has been completed successfully!",f"Deleted messages no longer logged for `{server}`\nDeleted messages no longer yielded in {channel.mention}"))

        elif arg == "-a":
            cursor.execute(f"SELECT * FROM servers WHERE guild_id={ctx.guild.id}")

            if not cursor.fetchone():
                try:
                    c = client.get_channel(int(channel_id))
                    if c == None:
                        await ctx.send(embed=error_embed("Invalid channel ID","The `<channel_id>` you have entered is not valid."))

                    else:
                        if str(client.get_channel(int(channel_id)).guild) != str((client.get_guild(ctx.guild.id)).name):
                            await ctx.send(embed=error_embed(f"Invalid channel ID `({channel_id})`","Please enter a channel ID __within__ the server.\nChannels from other servers cannot be used."))

                        else:
                            cursor.execute(f"INSERT INTO servers VALUES ({ctx.guild.id}, {channel_id})")
                            await ctx.send(embed=success_embed("Action has been completed successfully!",f"All deleted messages in `{ctx.guild.name}` are logged in {client.get_channel(int(channel_id)).mention}"))
                            connect.commit()

                except ValueError:
                        await ctx.send(embed=error_embed("Incorrect data type.","`<channel_id>` only accepts number data types! (You can't enter words)"))

            else:
                cursor.execute(f"SELECT channel_id FROM servers WHERE guild_id={ctx.guild.id}")
                channel = client.get_channel(cursor.fetchone()[0])
                await ctx.send(embed=error_embed("Existing Logging Channel",f"{channel.mention} has already been set for the deleted-message logger.\nYou can update it with `$delchannel -u <channel_id>`"))

            connect.close()

        else:
            ...

if __name__ == '__main__':
    with open("files/token.json","r") as f:
        client.run(json.load(f))
    