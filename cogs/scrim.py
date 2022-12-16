import os, asyncio
from discord.ext import commands, tasks
from utils import notification

discord_server_id = int(os.environ['discord_server_id'])
signup_channel_id = int(os.environ['signup_channel_id'])
signup_message_id = int(os.environ['signup_message_id'])
tier1_role_id  = int(os.environ['tier1_role_id'])
tier2_role_id = int(os.environ['tier2_role_id'])
fill_role_id = int(os.environ['fill_role_id'])

class Scrim(commands.Cog, description="Commands to organise scrim sign up"):
    def __init__(self, bot):
        self.bot = bot
        self.checkinopen = False
        self.teamlist = []
      
    @commands.Cog.listener()
    async def on_ready(self):
        self.scrim_signup.start()

    @tasks.loop(minutes=1)
    async def scrim_signup(self):
        #secondsleft = dates_time.seconds_until(23, 00)
        secondsleft = 5
        notification.printcon(f"{secondsleft}secs until scrim signup")
        await asyncio.sleep(secondsleft)
        channel = self.bot.get_channel(signup_channel_id)
        signupmsg = await channel.fetch_message(signup_message_id)
        if signupmsg:
            await signupmsg.edit(embed=notification.openscrims())
        else:
            signupmsg = await channel.send(embed=notification.openscrims())
        self.checkinopen = True
        #await asyncio.sleep(dates_time.seconds_until(6, 00))
        await asyncio.sleep(45)
        self.checkinopen = False
        #self.teamlist.clear()
        await signupmsg.edit(embed=notification.closescrims())

    @commands.command(name="checkin", brief="Check in a team or Mix")
    async def checkin(self, ctx):
        signupmsg = await ctx.fetch_message(signup_message_id)
        user = ctx.message.author
        await ctx.message.delete()
        teams = ""
      
        if not self.checkinopen:
            await notification.send_alert(ctx=ctx, header="Scrims are not open",content="You can not check in right now")
            return
                  
        if len(ctx.message.role_mentions) != 0:
            team_tag = ctx.message.role_mentions[0] 
            self.teamlist.append(team_tag)
        else: 
            team_tag = None
            fill_role = ctx.guild.get_role(fill_role_id)
            self.teamlist.append(fill_role)
          
        for slot, team in enumerate(self.teamlist):
            teams += "Slot {}: {}\n".format(slot+3, team.mention)
            print(teams)

        await signupmsg.edit(embed=notification.openscrims(teams))
        
async def setup(bot):
    await bot.add_cog(Scrim(bot))