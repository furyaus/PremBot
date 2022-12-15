import os, asyncio
from discord.ext import commands, tasks
from utils import dates_time, notification

discord_server_id = int(os.environ['discord_server'])
signup_channel_id = int(os.environ['signup_channel'])

def openscrims():
    response_msg = notification.respmsg()
    response_msg.add_field(name="Scrim Signup", value="Please remember the latest you can check out is: ```Weekday: 5:30pm AEST\nWeekend: 5:00pm AEST```**Or you'll be given a strike!**\n", inline=False)
    response_msg.add_field(name="Check In - oceanic team:", value="```Example```", inline=False)
    response_msg.add_field(name="Check In - fill team:", value="```Example```", inline=False)
    response_msg.timestamp = dates_time.get_nowutc()
    notification.printcon("Scrims are open")
    return response_msg

def closescrims():
    response_msg = notification.respmsg()
    response_msg.add_field(name="Sign ups are closed", value="```Example```", inline=False)
    response_msg.timestamp = dates_time.get_nowutc()
    notification.printcon("Scrims are closed")
    return response_msg

class Scrim(commands.Cog, description="Commands to organise scrim sign up"):
    def __init__(self, bot):
        self.bot = bot
      
    @commands.Cog.listener()
    async def on_ready(self):
        self.scrim_signup.start()
    
    @tasks.loop(seconds=10)
    async def scrim_signup(self):
        secondsleft = dates_time.seconds_until(23, 00)
        notification.printcon(f"{secondsleft} until scrim signup")
        await asyncio.sleep(secondsleft)
        channel = self.bot.get_channel(signup_channel_id)
        signupmsg = await channel.send(embed=openscrims())
        reactions = ['✅']
        for emoji in reactions: 
            await signupmsg.add_reaction(emoji)
        await asyncio.sleep(dates_time.seconds_until(6, 00))
        await signupmsg.edit(embed=closescrims())
          
    # @bot.event
    # async def on_reaction_add(reaction, user):
    # if reaction.message == msg:
    #     some_list.append(user)
      
async def setup(bot):
    await bot.add_cog(Scrim(bot))