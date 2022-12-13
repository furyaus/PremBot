# PremBot
# Version: 0.1
# Date: 31.10.22
# Current Authors: fury#1662
# Github: https://github.com/furyaus/prembot
# Repl.it: https://replit.com/@furyaus/prembot
# Credit to Speedy from EU PUBG: https://github.com/mihawk123/DiscordScrimBot

import os, discord
from discord.ext import commands

# Global variables
clientintents = discord.Intents.all()
clientintents.members = True
#my_token = os.environ['bot_token']
my_token = os.getenv('bot_token')
client = commands.Bot(command_prefix=".", intents=clientintents)

# Report Bot is running
@client.event
async def on_ready():
    print(str(client.user)+" running ")

# Hello to DMs
@client.event
async def on_message(message):
    if message.author != client.user:
        if message.content.startswith('.hello'):
            await message.channel.send('Hello!')

# Hello any channel
@client.command()
async def hello(ctx):
    await ctx.send('hello!')

# Run the bot
try:
    client.run(my_token)
except:
    os.system("kill 1")
