# PremBot
# Version: 0.4
# Date: 13.12.22
# Current Authors: fury#1662
# Github: https://github.com/furyaus/prembot
# Repl.it: https://replit.com/@furyaus/PremBot
# Credit to Speedy from EU PUBG: https://github.com/mihawk123/DiscordScrimBot

import os, discord, asyncio
from discord import Activity
from discord.ext import commands
from pretty_help import PrettyHelp

# Global tokens
bot_token = os.environ['bot_token']
clientintents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=clientintents, help_command=PrettyHelp())

# Load cogs
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await client.load_extension(f"cogs.{filename[:-3]}")
            print(filename+' loaded successfully')

# Report Bot is running
@client.event
async def on_ready():
    status = Activity(name="!help", type=2)
    await client.change_presence(activity=status)
    print(str(client.user)+" is ready\n")

# Run the bot
async def main():
    async with client:
        await load_extensions()
        try:
          await client.start(bot_token)
        except:
          os.system("kill 1")
asyncio.run(main())