import discord
from utils import notification, dates_time
from discord.ext import commands
from requests import get
  
class Tools(commands.Cog, description="Commands to confirm bot is OK"):
    def __init__(self, bot):
        self.bot = bot
      
    # Repond to ping
    @commands.command(name="status", brief="Return response", description="Send ping with IP")
    @commands.has_guild_permissions(administrator=True)
    async def status(self, ctx):
        await ctx.message.delete()
        response_msg = notification.respmsg()
        ip = get('https://api.ipify.org').text
        response_msg.add_field(name="Ping", value=ip, inline=False)
        response_msg.timestamp = dates_time.get_nowutc()
        notification.printcon(f"PremBot was pinged by {ctx.message.author}")
        await ctx.message.author.send(embed=response_msg)
      
    # Inspire any channel
    @commands.command(name="inspire", brief="Collect Quote", description="Post Quote")
    async def inspire(self, ctx):
        response_msg = notification.respmsg()
        response_msg.add_field(name="Quote", value=notification.quote(), inline=False)
        response_msg.timestamp = dates_time.get_nowutc()
        notification.printcon(f"PremBot Inspired {ctx.message.author}")
        await ctx.message.channel.send(embed=response_msg)
      
   # No DMs
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if isinstance(message.channel, discord.DMChannel):
            response_msg = notification.respmsg()
            response_msg.add_field(name="Private Messages", value="No DM's", inline=False)
            response_msg.timestamp = dates_time.get_nowutc()
            await message.channel.send(embed=response_msg)
            notification.printcon(f"Auto Reply Message send to {message.author}")
      
async def setup(bot):
    await bot.add_cog(Tools(bot))