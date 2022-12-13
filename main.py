# PremBot
# Version: 0.1
# Date: 31.10.22
# Current Authors: fury#1662
# Github: https://github.com/furyaus/prembot
# Repl.it: https://replit.com/@furyaus/prembot
# Credit to Speedy from EU PUBG: https://github.com/mihawk123/DiscordScrimBot

import os, discord, json, requests
from discord import Activity
from discord.ext import commands
from discord.ext.commands import Bot
from discord import Intents

from utils.MySQLCon import MySQLCon
from utils.Checks import Checks
from utils import Notification

print("Bot is starting...")

BOT_PREFIX = "!"
TOKEN = os.getenv('bot_token')
HOST = os.getenv('host')
USER = os.getenv('user')
PASSWORD = os.getenv('password')
DATABASE = os.getenv('database')

extensions = ["cogs.Settings", "cogs.Scrim", "cogs.Pinger", "cogs.Util"]

intents = Intents.default()
intents.members = True

client = Bot(command_prefix=BOT_PREFIX, intents=intents)
client.db = MySQLCon(HOST, USER, PASSWORD, DATABASE)
client.prefix = BOT_PREFIX
client.checks = Checks(client=client)

if __name__ == 'main':
    for extension in extensions:
        try:
            client.load_extension(extension)
            print('{} loaded successfully'.format(extension))
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))

@client.event
async def on_guild_join(guild):
    print("Bot joined server: " + guild.name + "<" + str(guild.id) + ">")
    client.db.init_server(guild.id, guild.name)

#@client.check
#async def globally_block_dms(ctx):
#    return ctx.guild is not None

#@client.check
#async def globally_block_bot(ctx):
#    return not ctx.author.bot

@client.command(name="restart", brief="reconnect to database")
@commands.has_guild_permissions(administrator=True)
async def reconnect_db(ctx):
    await ctx.message.delete()
    client.db = MySQLCon(HOST, USER, PASSWORD, DATABASE)
    await Notification.send_approve(ctx, description="Reconnected to database")

# Collect quotes
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
    status = Activity(name=BOT_PREFIX + "help", type=2)
    await client.change_presence(activity=status)
    print(str(client.user)+" is ready\n")

# Run the bot
client.run(TOKEN, bot=True, reconnect=True)