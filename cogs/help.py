from discord.ext import commands
from utils import notification

class Help(commands.Cog):
    def __init__(self, bot):
       self.bot = bot

    # Help
    @commands.command()
    async def help(self, ctx):
        response_msg = notification.respmsg("Help for PremBot","PremBot schedule scrims and organises lobbies for APAC")
        response_msg.add_field(name="Scrim signup",value="How to checkin and checkout of scrims```!scrimhelp```",inline=False)
        response_msg.add_field(name="Team roles",value="How to add and remove players from team rosters```!rolehelp```",inline=False)
        response_msg.add_field(name="Bot tools",value="Extra tools that bot has to help```!toolshelp```",inline=False)
        response_msg.add_field(name="Admin help",value="How to admin the bot and setup```!adminhelp```",inline=False)
        response_msg.add_field(name="Report issues",value="Head to github and create a new issue or feature request [https://github.com/furyaus/PremBot/issues](https://github.com/furyaus/PremBot/issues)",inline=False)
        await ctx.message.channel.send(embed=response_msg)

    #Scrim Help
    @commands.command()
    async def scrimhelp(self, ctx):
        response_msg = notification.respmsg("Scrim Help","How to check in or out for APAC Prem scrims")
        response_msg.add_field(name="Fill team checkin",value="Checks in a fill team ```!checkin```",inline=False)
        response_msg.add_field(name="Fill team checkout",value="Checks in a team (must have core 2) ```!checkin @VIP```",inline=False)
        response_msg.add_field(name="Team checkin",value="Checks out a fill team ```!checkout```",inline=False)
        response_msg.add_field(name="Team checkout",value="Checks out a team ```!checkout @VIP```",inline=False)
        response_msg.add_field(name="Late fill team checkout",value="Checks out a fill team with a strike ```!checkout```",inline=False)
        response_msg.add_field(name="Late team checkout",value="Checks out a team with a strike ```!checkout @VIP```",inline=False)
        response_msg.add_field(name="Report issues",value="Head to github and create a new issue or feature request [https://github.com/furyaus/PremBot/issues](https://github.com/furyaus/PremBot/issues)",inline=False)
        await ctx.message.channel.send(embed=response_msg)

    #Role Help
    @commands.command()
    async def rolehelp(self, ctx):
        response_msg = notification.respmsg("Scrim Help","How to check in or out for APAC Prem scrims")
        response_msg.add_field(name="Create a team",value="Create a new team ```!createteam VIP```",inline=False)
        response_msg.add_field(name="Delete a team",value="Delete a current team ```!deleteteam VIP```",inline=False)
        response_msg.add_field(name="Add a player",value="Add a player to team roster ```!addplayer @fury @VIP```",inline=False)
        response_msg.add_field(name="Remove a player",value="Remove a player to team roster ```!removeplayer @fury @VIP```",inline=False)
        response_msg.add_field(name="Report issues",value="Head to github and create a new issue or feature request [https://github.com/furyaus/PremBot/issues](https://github.com/furyaus/PremBot/issues)",inline=False)
        await ctx.message.channel.send(embed=response_msg)

    #Tools Help
    @commands.command()
    async def toolshelp(self, ctx):
        response_msg = notification.respmsg("Scrim Help","How to check in or out for APAC Prem scrims")
        response_msg.add_field(name="Status",value="Sends a PM with current bot IP to confirm running```!status```",inline=False)
        response_msg.add_field(name="Inspiration",value="Sends a inspiring quote to current channel - good way to confirm bot has internet access ```!inspire```",inline=False)
        response_msg.add_field(name="No DMs to or from PremBot",value="Bot repsonds to DMs with ```No DMs```",inline=False)
        response_msg.add_field(name="Report issues",value="Head to github and create a new issue or feature request [https://github.com/furyaus/PremBot/issues](https://github.com/furyaus/PremBot/issues)",inline=False)
        await ctx.message.channel.send(embed=response_msg)
    
    # Admin help
    @commands.command()
    async def adminhelp(self, ctx):
        response_msg = notification.respmsg("Admin help for Rank Bot","Admin users can remove users and call for global updates.")
        response_msg.add_field(name=".linked",value="Returns the total number of currently stored users in JSON file. ```.linked```",inline=False)
        response_msg.add_field(name=".say",value="Allows admin to message any channel. Can take channel name or channel ID. Look out for icons when using channel name. 1024 character limit. ```.say channel_name message```",inline=False)
        response_msg.add_field(name="Report issues",value="Head to github and create a new issue or feature request [https://github.com/furyaus/PremBot/issues](https://github.com/furyaus/PremBot/issues)",inline=False)
        await ctx.message.channel.send(embed=response_msg)

async def setup(bot):
    await bot.add_cog(Help(bot))