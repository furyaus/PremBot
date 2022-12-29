import os, asyncio
from discord.ext import commands, tasks
from utils import notification, dates_time

discord_server_id = int(os.environ['discord_server_id'])
bot_admin_channel_id = int(os.environ['bot_admin_channel_id'])
signup_channel_id = int(os.environ['signup_channel_id'])
lobby1_channel_id = int(os.environ['lobby1_channel_id'])
signup_message_id = int(os.environ['signup_message_id'])
lobby1_message_id = int(os.environ['lobby1_message_id'])
tier1_role_id  = int(os.environ['tier1_role_id'])
tier2_role_id = int(os.environ['tier2_role_id'])
tier3_role_id = int(os.environ['tier3_role_id'])

class Scrim(commands.Cog, description="Commands to organise scrim sign up"):
    def __init__(self, bot):
        self.bot = bot
        self.checkinopen = False
        self.checkoutclosed = False
        self.teamcount = 0
        self.t1 = []
        self.t2 = []
        self.t3 = []
        self.fill = []

    def teamlist(self):
        teamstr = ""
        if self.t1 or self.t2 or self.t3 or self.fill:
              for slot, team in enumerate(self.t1):
                  teamstr += "Slot {}: {}\n".format(slot+3, team.mention)
              for slot, team in enumerate(self.t2):
                  teamstr += "Slot {}: {}\n".format(len(self.t1)+slot+3, team.mention)
              for slot, team in enumerate(self.t3):
                  teamstr += "Slot {}: {}\n".format(len(self.t1)+len(self.t2)+slot+3, team.mention)
              for slot, user in enumerate(self.fill):
                  teamstr += "Slot {}: {} fill team\n".format(len(self.t1)+len(self.t2)+len(self.t3)+slot+3, user.mention)
        else:
            teamstr = ""
        return teamstr
  
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

        if self.teamcount > 13:
            await lobby1msg.edit(embed=notification.postlobby(self.teamlist()))
            notification.printcon("Post lobbies in lobby channel")
        else:
            await lobby1msg.edit(embed=notification.cancellobby(self.teamlist()))
            notification.printcon(f"Scrims cancelled - {self.teamcount} teams")

        self.t1.clear()
        self.t2.clear()
        self.t3.clear()
        self.fill.clear()

    @commands.command(name="checkin", brief="Check in a team or Mix")
    async def checkin(self, ctx):
        signupmsg = await ctx.fetch_message(signup_message_id)
        user = ctx.message.author
        t1role = ctx.guild.get_role(tier1_role_id)
        t2role = ctx.guild.get_role(tier2_role_id)
        t3role = ctx.guild.get_role(tier3_role_id)
        await ctx.message.delete()
        self.teamcount += 1
      
        if not self.checkinopen:
            await notification.send_alert(ctx=ctx, header="Scrims are not open",content="You can not check in right now")
            return
                  
        if len(ctx.message.role_mentions) != 0:
            team_tag = ctx.message.role_mentions[0]
            if t1role in ctx.author.roles:
                self.t1.append(team_tag)
                notification.printcon(f"{team_tag} team has checked in for T1")
            if t2role in ctx.author.roles:
                self.t2.append(team_tag)
                notification.printcon(f"{team_tag} team has checked in for T2")
            if t3role in ctx.author.roles:
                self.t3.append(team_tag)
                notification.printcon(f"{team_tag} team has checked in for T3")
        else: 
            self.fill.append(user)
            notification.printcon(f"{user} fill team has checked in")
          
        await signupmsg.edit(embed=notification.openscrims(self.teamlist()))

    @commands.command(name="checkout", brief="Check out a team")
    async def checkout(self, ctx):
        signupmsg = await ctx.fetch_message(signup_message_id)
        user = ctx.message.author
        t1role = ctx.guild.get_role(tier1_role_id)
        t2role = ctx.guild.get_role(tier2_role_id)
        t3role = ctx.guild.get_role(tier3_role_id)
        await ctx.message.delete()
        self.teamcount -= 1
      
        if not self.checkinopen:
            await notification.send_alert(ctx=ctx, header="Scrims are not open",content="You can not check in right now")
            return

        if self.checkoutclosed:
            await notification.send_alert(ctx=ctx, header="Past check out time",content="You will be striked - type !latecheckout")
            return
      
        if len(ctx.message.role_mentions) != 0:
            team_tag = ctx.message.role_mentions[0] 
            if t1role in ctx.author.roles:
                self.t1.remove(team_tag)
                notification.printcon(f"{team_tag} team has checked in for T1")
            if t2role in ctx.author.roles:
                self.t2.remove(team_tag)
                notification.printcon(f"{team_tag} team has checked in for T2")
            if t3role in ctx.author.roles:
                self.t3.remove(team_tag)
                notification.printcon(f"{team_tag} team has checked in for T3")
        else: 
            self.fill.remove(user)
            notification.printcon(f"{user} fill team has checked out")

        if self.t1 or self.fill:
            await signupmsg.edit(embed=notification.openscrims(self.teamlist()))
        else:
            await signupmsg.edit(embed=notification.openscrims())

    @commands.command(name="latecheckout", brief="Late checkout of team")
    async def latecheckout(self, ctx):
        self.checkoutclosed = False
        user = ctx.message.author
        await self.checkout(ctx)
        botadminchannel = self.bot.get_channel(bot_admin_channel_id)
        if len(ctx.message.role_mentions) != 0:
            team_tag = ctx.message.role_mentions[0] 
            await botadminchannel.send(embed=notification.latecheckout(user.mention, team_tag.mention))
        else: 
            await botadminchannel.send(embed=notification.latecheckout(user.mention))
        notification.printcon(f"{user} has checkedout late")
        self.checkoutclosed = True

async def setup(bot):
    await bot.add_cog(Scrim(bot))