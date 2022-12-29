import os, asyncio
from discord.ext import commands, tasks
from utils import notification, dates_time

discord_server_id = int(os.environ['discord_server_id'])
signup_channel_id = int(os.environ['signup_channel_id'])
lobby1_channel_id = int(os.environ['lobby1_channel_id'])
signup_message_id = int(os.environ['signup_message_id'])
lobby1_message_id = int(os.environ['lobby1_message_id'])
tier1_role_id  = int(os.environ['tier1_role_id'])
tier2_role_id = int(os.environ['tier2_role_id'])
fill_role_id = int(os.environ['fill_role_id'])

class Scrim(commands.Cog, description="Commands to organise scrim sign up"):
    def __init__(self, bot):
        self.bot = bot
        self.checkinopen = False
        self.checkoutclosed = False
        self.teams = []
        self.fillteams = []
      
    @commands.Cog.listener()
    async def on_ready(self):
        self.scrim_signup.start()

    @tasks.loop(minutes=1)
    async def scrim_signup(self):
        #secondsleft = dates_time.seconds_until(23, 00)
        secondsleft = 5
        notification.printcon(f"{secondsleft}secs until scrim signup")
        await asyncio.sleep(secondsleft)
        signupchannel = self.bot.get_channel(signup_channel_id)
        lobby1channel = self.bot.get_channel(lobby1_channel_id)
        
        #first time, comment out fetch, uncomment send, and set secert msg id after post
        #signupmsg = await signupchannel.send(embed=notification.openscrims())
        signupmsg = await signupchannel.fetch_message(signup_message_id)
        await signupmsg.edit(embed=notification.openscrims())
        
        self.checkinopen = True
        #await asyncio.sleep(dates_time.seconds_until(6, 00))
        await asyncio.sleep(20)
        self.checkoutclosed = True
        notification.printcon("Checkout closed")
        await asyncio.sleep(20)
        self.checkinopen = False
        await signupmsg.edit(embed=notification.closescrims())

        #first time, comment out fetch, uncomment send, and set secert msg id after post
        #lobby1msg = await lobby1channel.send(embed=notification.postlobby(teamstr))
        lobby1msg = await lobby1channel.fetch_message(lobby1_message_id)
        teamstr = ""
        if self.teams or self.fillteams:
            for slot, team in enumerate(self.teams):
                teamstr += "Slot {}: {}\n".format(slot+3, team.mention)
            for slot, user in enumerate(self.fillteams):
                teamstr += "Slot {}: {} fill team\n".format(len(self.teams)+slot+3, user.mention)

        if len(self.teams)+len(self.fillteams) > 13:
            await lobby1msg.edit(embed=notification.postlobby(teamstr))
            notification.printcon("Post lobbies in lobby channel")
        else:
            if self.teams or self.fillteams: 
                await lobby1msg.edit(embed=notification.cancellobby(teamstr))
            else:
                await lobby1msg.edit(embed=notification.cancellobby())
            notification.printcon(f"Scrims cancelled - {len(self.teams)+len(self.fillteams)} teams")

        self.teams.clear()
        self.fillteams.clear()

    @commands.command(name="checkin", brief="Check in a team or Mix")
    async def checkin(self, ctx):
        signupmsg = await ctx.fetch_message(signup_message_id)
        user = ctx.message.author
        await ctx.message.delete()
        teamstr = ""
      
        if not self.checkinopen:
            await notification.send_alert(ctx=ctx, header="Scrims are not open",content="You can not check in right now")
            return
                  
        if len(ctx.message.role_mentions) != 0:
            team_tag = ctx.message.role_mentions[0] 
            self.teams.append(team_tag)
            notification.printcon(f"{team_tag} team has checked in")
        else: 
            self.fillteams.append(user)
            notification.printcon(f"{user} fill team has checked in")
          
        for slot, team in enumerate(self.teams):
            teamstr += "Slot {}: {}\n".format(slot+3, team.mention)
        for slot, user in enumerate(self.fillteams):
            teamstr += "Slot {}: {} fill team\n".format(len(self.teams)+slot+3, user.mention)

        await signupmsg.edit(embed=notification.openscrims(teamstr))

    @commands.command(name="checkout", brief="Check out a team")
    async def checkout(self, ctx):
        signupmsg = await ctx.fetch_message(signup_message_id)
        user = ctx.message.author
        await ctx.message.delete()
        teamstr = ""
      
        if not self.checkinopen:
            await notification.send_alert(ctx=ctx, header="Scrims are not open",content="You can not check in right now")
            return

        if self.checkoutclosed:
            await notification.send_alert(ctx=ctx, header="Past check out time",content="You will be striked - type !latecheckout")
            return
      
        if len(ctx.message.role_mentions) != 0:
            team_tag = ctx.message.role_mentions[0] 
            self.teams.remove(team_tag)
            notification.printcon(f"{team_tag} team has checked out")
        else: 
            self.fillteams.remove(user)
            notification.printcon(f"{user} fill team has checked out")

        if self.teams or self.fillteams:
            for slot, team in enumerate(self.teams):
                teamstr += "Slot {}: {}\n".format(slot+3, team.mention)
            for slot, user in enumerate(self.fillteams):
                teamstr += "Slot {}: {} fill team\n".format(len(self.teams)+slot+3, user.mention)
              
            await signupmsg.edit(embed=notification.openscrims(teamstr))
        else:
            await signupmsg.edit(embed=notification.openscrims())

    @commands.command(name="latecheckout", brief="Late checkout of team")
    async def latecheckout(self, ctx):
        self.checkoutclosed = False
        user = ctx.message.author
        notification.printcon(f"{user} has checkedout late")
        await self.checkout(ctx)
        self.checkoutclosed = True

        
async def setup(bot):
    await bot.add_cog(Scrim(bot))