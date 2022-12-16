import os, asyncio
from discord.ext import commands, tasks
from utils import notification

discord_server_id = int(os.environ['discord_server_id'])
signup_channel_id = int(os.environ['signup_channel_id'])
signup_message_id = int(os.environ['signup_message_id'])
tier1_role = int(os.environ['tier1_role'])
tier2_role = int(os.environ['tier2_role'])

class Scrim(commands.Cog, description="Commands to organise scrim sign up"):
    def __init__(self, bot):
        self.bot = bot
      
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
        #self.bot.checkinopen = True
        #await asyncio.sleep(dates_time.seconds_until(6, 00))
        await asyncio.sleep(20)
        #self.bot.checkinopen = False
        await signupmsg.edit(embed=notification.closescrims())

    @commands.command(name="checkin", brief="Check in a team or Mix")
    async def checkin(self, ctx):
        await ctx.message.delete()
        teir_tag = None
        member_tag = None
        if len(ctx.message.role_mentions) != 0: teir_tag = ctx.message.role_mentions[0]
        if len(ctx.message.mentions) != 0: member_tag = ctx.message.mentions[0]
        print(teir_tag)
        print(member_tag)
      
        if teir_tag is None and member_tag is None:
            await notification.send_alert(ctx=ctx, header="No team or member tagged", content="Use:\n{}checkin <@your team>\nor\n{}checkin <@yourself>""".format(self.client.prefix, self.client.prefix))
            return

        if not self.bot.checkinopen:
            await notification.send_alert(ctx=ctx, header="Scrims are not open",content="You can not check in right now")
            return

      
async def setup(bot):
    await bot.add_cog(Scrim(bot))