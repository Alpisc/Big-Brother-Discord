import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import typing
import requests
from io import BytesIO

load_dotenv()
TOKEN = os.getenv("TOKEN")
WELCOMECHANNELID = int(os.getenv("WELCOMECHANNELID"))
RULECHANNELID = int(os.getenv("RULECHANNELID"))
USERROLEID = int(os.getenv("USERROLEID"))
EDITEDLOGCHANNELID = int(os.getenv("EDITEDLOGCHANNELID"))
DELETEDLOGCHANNELID = int(os.getenv("DELETEDLOGCHANNELID"))

client = commands.Bot(command_prefix="-", intents=discord.Intents.all())

@client.event
async def on_ready():
    await client.tree.sync()
    await client.change_presence(activity=discord.activity.Activity(type=discord.ActivityType.watching, name="You"), status=discord.Status.do_not_disturb)
    print(f"{client.user.name} has connected to Discord!")

@client.event
async def on_member_join(member):
    channel = client.get_channel(WELCOMECHANNELID)
    await channel.send(f"Welcome to the server {member.mention}! Make sure to read the {client.get_channel(RULECHANNELID).mention} and have fun!")
    role = discord.utils.get(member.guild.roles, id=USERROLEID)
    await member.add_roles(role)

@client.event
async def on_member_remove(member):
    channel = client.get_channel(WELCOMECHANNELID)
    await channel.send(f"{member.mention} has left the server")

@client.event
async def on_message_edit(before, after):
    if before.content != after.content:
        channel = client.get_channel(EDITEDLOGCHANNELID)
        embed = discord.Embed(title=f"Message edited in {before.channel.mention}", timestamp=after.created_at)
        embed.set_author(name=before.author, url=after.jump_url , icon_url=before.author.display_avatar.url)
        embed.add_field(name="Before", value=before.clean_content, inline=False)
        embed.add_field(name="After", value=after.clean_content, inline=False)
        await channel.send(embed=embed)

@client.event
async def on_message_delete(message):
    channel = client.get_channel(DELETEDLOGCHANNELID)
    embed = discord.Embed(title=f"Message deleted in {message.channel.mention}", timestamp=message.edited_at)
    embed.set_author(name=message.author, icon_url=message.author.display_avatar.url)
    embed.add_field(name="", value=message.clean_content, inline=False)
    await channel.send(embed=embed)



@client.tree.command(name="ping", description="Shows the bot's latency")
async def _ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong!... {round(client.latency * 1000)}ms")

@client.tree.command(name="move", description="Moves all members between voice channels")
async def _move(interaction: discord.Interaction, from_channel: discord.VoiceChannel, to_channel: discord.VoiceChannel):
    if interaction.user.guild_permissions.move_members:
        for member in from_channel.members:
            await member.move_to(to_channel)
        await interaction.response.send_message(f"Moved all members from {from_channel.mention} to {to_channel.mention}")
    else:
        await interaction.response.send_message("You do not have the permissions to use this command", ephemeral=True)

@client.tree.command(name="mute", description="Mutes a member")
async def _mute(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.guild_permissions.mute_members:
        await member.edit(mute=True)
        await interaction.response.send_message(f"Muted {member.mention}")
    else:
        await interaction.response.send_message("You do not have the permissions to use this command", ephemeral=True)

@client.tree.command(name="unmute", description="Unmutes a member")
async def _unmute(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.guild_permissions.mute_members:
        await member.edit(mute=False)
        await interaction.response.send_message(f"Unmuted {member.mention}")
    else:
        await interaction.response.send_message("You do not have the permissions to use this command", ephemeral=True)

@client.tree.command(name="rename", description="Renames a member")
async def _rename(interaction: discord.Interaction, member: discord.Member, *, name: str):
    if interaction.user.guild_permissions.manage_nicknames:
        await member.edit(nick=name)
        await interaction.response.send_message(f"Renamed {member.mention} to {name}")
    else:
        await interaction.response.send_message("You do not have the permissions to use this command", ephemeral=True)

@client.tree.command(name="purge", description="Purges a specified amount of messages")
async def _purge(interaction: discord.Interaction, amount: int):
    if interaction.user.guild_permissions.manage_messages:
        await interaction.channel.purge(limit=amount)
        msg = await interaction.response.send_message(f"Purged {amount} messages", ephemeral=True)
    else:
        await interaction.response.send_message("You do not have the permissions to use this command", ephemeral=True)

@client.tree.command(name="avatar", description="Shows a member's avatar")
async def _avatar(interaction: discord.Interaction, member: typing.Optional[discord.Member]):
    if member is None:
        member = interaction.user

    image_data = requests.get(member.avatar_url).content
    await interaction.response.send_message(file=discord.File(BytesIO(image_data), 'profile_picture.png'))

client.run(TOKEN)
