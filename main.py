# PremBot
# Version: 0.4
# Date: 13.12.22
# Current Authors: fury#1662
# Github: https://github.com/furyaus/prembot
# Repl.it: https://replit.com/@furyaus/PremBot
# Credit to Speedy from EU PUBG: https://github.com/mihawk123/DiscordScrimBot

import os, discord, asyncio, traceback
from utils import notification
from discord import Activity
from discord.ext import commands
from pretty_help import PrettyHelp

# Global tokens
bot_token = os.environ['bot_token']
botintents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=botintents, help_command=PrettyHelp())
bot_log_channel_id = int(os.environ['bot_log_channel_id'])

# Load cogs
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await bot.load_extension(f"cogs.{filename[:-3]}")
            notification.printcon(filename+" loaded successfully")

# Report Bot is running
@bot.event
async def on_ready():
    status = Activity(name="!help", type=2)
    await bot.change_presence(activity=status)
    notification.printcon(f"{bot.user.name} is online and ready!\n")

# Catch unknown commands
@bot.event
async def on_command_error(ctx, error):
    msg = ctx.message.content
    await ctx.message.delete()
    await notification.send_alert(ctx=ctx, header=f"Command {msg} not found",content="Try again or type !help")
    logchannel = bot.get_channel(bot_log_channel_id)
    response_msg = notification.respmsg()
    response_msg.description = "Command Error"
    response_msg.add_field(name="Error",value=f"An error occured: {str(error)}",inline=False)
    await logchannel.send(embed=response_msg)

# Let admin know about errors
@bot.event
async def on_error(event, *args, **kwargs):
    logchannel = bot.get_channel(bot_log_channel_id)
    response_msg = notification.respmsg()
    response_msg.description = event
    response_msg.add_field(name='Event',value='```py\n%s\n```' % traceback.format_exc())
    await logchannel.send(embed=response_msg)

# Run the bot
async def main():
    async with bot:
        await load_extensions()
        try:
          await bot.start(bot_token)
        except:
          os.system("kill 1")
asyncio.run(main())