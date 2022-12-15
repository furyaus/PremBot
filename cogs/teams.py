import discord, datetime, asyncio
from discord.ext import commands
from utils import notification

mix_term = "We require following information to verify your account:\n1. Link your steam profile (visibility of pubg game time)\n2. Link your pubg.op.gg account\n3. Twire.gg link of recent tournaments (recent 1 year) that you played (name of round/group/team)\n4. Your server discord name must match with your pubg IGN\n\nWe will decline your request if:\n-Your discord account was recently created and/or shares no mutal competitive discord servers\n-Your steam account has a VAC ban (<1 year) and/or has very little pubg game time\n-Your pubg.op.gg link shows no ranked activity\n-You cant provide any recent tournament links"

green = 0x11f711
red = 0xD10000
orange = 0xff8800
blue = 0x007BFD

num_to_symbol = {
    1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣', 6: '6️⃣',
    7: '7️⃣', 8: '8️⃣', 9: '9️⃣'
}

class Teams(commands.Cog, description="Commands to add, update and remove roles for teams"):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Teams(bot))