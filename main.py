import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

client = commands.Bot(command_prefix='-', intents=discord.Intents.all())

@client.event
async def on_ready():
    await client.tree.sync()
    await client.change_presence(activity=discord.activity.Activity(type=discord.ActivityType.watching, name='You'), status=discord.Status.do_not_disturb)
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    channel = client.get_channel(1185982616315371560)
    await channel.send(f'Welcome to the server {member.mention}! Make sure to read the {client.get_channel(1185997047766196335).mention} and have fun!')
    role = discord.utils.get(member.guild.roles, id=1185980965340852414)
    await member.add_roles(role)

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

client.run(TOKEN)
