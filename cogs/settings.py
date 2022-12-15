from discord.ext import commands

from utils import checks
from utils import notification

class Settings(commands.Cog, description="Commands for bot settings"):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="settings", invoke_without_command=True)
    @commands.has_guild_permissions(administrator=True)
    async def setting_command(self, ctx):
        pass

    @setting_command.group(name="admin", invoke_without_command=True)
    @commands.has_guild_permissions(administrator=True)
    async def setting_admin(self, ctx):
        pass

    @setting_admin.command(name="add")
    @commands.has_guild_permissions(administrator=True)
    @commands.check(checks.role_mentioned)
    async def setting_add_admin(self, ctx):
        print("Adding admin role to server:" + ctx.guild.name)


    @setting_admin.command(name="remove")
    @commands.check(checks.role_mentioned)
    @commands.has_guild_permissions(administrator=True)
    async def setting_remove_admin(self, ctx):
        print("Removing admin role from server:" + ctx.guild.name)


async def setup(bot):
    await bot.add_cog(Settings(bot))