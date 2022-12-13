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

def quote():
    request = requests.get("https://leksell.io/zen/api/quotes/random")
    json_data = json.loads(request.text)
    quote = json_data['quote'] + " -" + json_data['author']
    if request.status_code != 200:
        request = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(request.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote

# Respond to DMs
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if isinstance(message.channel,discord.DMChannel):
        await message.channel.send("No private messages while at work")
    await client.process_commands(message)

# Hello any channel
@client.command()
async def hello(ctx):
    await ctx.send('hello!')

# Inspire the channel
@client.command()
async def inspire(ctx):
    await ctx.send(quote())

# Report Bot is running
@client.event
async def on_ready():
    print(str(client.user)+" is ready\n")
  
# Run the bot
try:
    client.run(my_token)
except:
    os.system("kill 1")
