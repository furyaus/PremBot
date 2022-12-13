import discord, json, requests, datetime
from builtins import print
from utils import notification
from discord.ext import commands
from requests import get

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
  
class Alive(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.command(name="status", brief="Return response", description="Send ping with IP")
    @commands.has_guild_permissions(administrator=True)
    # Repond to ping
    async def status(self, ctx):
        await ctx.message.delete()
        response_msg = notification.botHelper.respmsg()
        fury = "fury#1119"
        user = ctx.message.author.name + '#' + ctx.message.author.discriminator
        if user == fury:
            time = datetime.datetime.now().strftime("%H:%M")
            print(f"{time} | PremBot was pinged")
            ip = get('https://api.ipify.org').text
            response_msg.add_field(name="Quote", value=ip, inline=False)
            response_msg.timestamp = datetime.datetime.utcnow()
            await ctx.message.author.send(embed=response_msg)
      
    # Inspire any channel or DM
    @commands.command(name="inspire", brief="Collect Quote", description="Post Quote")
    async def inspire(self, ctx):
        response_msg = notification.botHelper.respmsg()
        time = datetime.datetime.now().strftime("%H:%M")
        print(f"{time} | PremBot Inspired Someone")
        response_msg.add_field(name="Quote", value=quote(), inline=False)
        response_msg.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=response_msg)
  
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return # Exiting if the author of the message is ourself
        if isinstance(message.channel, discord.DMChannel) and not message.startswith('.'):
            response_msg = notification.botHelper.respmsg()
            response_msg.add_field(name="Quote", value="No DM's", inline=False)
            response_msg.timestamp = datetime.datetime.utcnow()
            await message.channel.send(embed=response_msg)
            time = datetime.datetime.now().strftime("%H:%M")
            print(f"{time} | Auto Reply Message send to {message.author}")
      
async def setup(client):
    await client.add_cog(Alive(client))