import discord, json, requests
from builtins import print

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
  
class alive(commands.Cog):
    def __init__(self, client):
        pass

    @commands.command(name="status", brief="Return response", description="Send ping with IP")
    @commands.has_guild_permissions(administrator=True)
    # Repond to ping
    async def status(self, ctx):
        await ctx.message.delete()
        fury = "fury#1119"
        user = ctx.message.author.name + '#' + ctx.message.author.discriminator
        if user == fury:
            print("PremBot was pinged ")
            ip = get('https://api.ipify.org').text
            await ctx.message.author.send(ip)

    # Inspire any channel or DM
    @commands.command(name="inspire", brief="Collect Quote", description="Post Quote")
    async def inspire(self, ctx):
        await ctx.send(quote())
      
    @commands.command()  
    async def on_message(self, message):
        if message.author == alive.user:
            return
        if isinstance(message.channel,discord.DMChannel):
            await message.channel.send("No DM's")
        await alive.process_commands(message)

async def setup(client):
    await client.add_cog(alive(client))