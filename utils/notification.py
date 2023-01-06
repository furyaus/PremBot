import discord, json, requests
from utils import dates_time

def printcon(content):
    print(f"{dates_time.get_now()} | "+content)

def printlog(content):
    response_msg = respmsg("Bot Log")
    response_msg.add_field(name="Log", value=content, inline=False)
    return response_msg

def respmsg(titleText=None, descText=None):
    if (titleText == None and descText == None):
        response_msg = discord.Embed(colour=discord.Colour.green())
        printcon("Sent respmsg with no title")
    if (titleText != None and descText == None):
        response_msg = discord.Embed(colour=discord.Colour.green(),title=titleText)
        printcon(titleText)
    if (titleText == None and descText != None):
        response_msg = discord.Embed(colour=discord.Colour.green(),description=descText)
        printcon("Sent respmsg with no title")
    if (titleText != None and descText != None):
        response_msg = discord.Embed(colour=discord.Colour.green(),title=titleText,description=descText)
        printcon(titleText)
    response_msg.set_thumbnail(url="https://i.ibb.co/GCTgdsz/premlogo-100px.png")
    response_msg.timestamp = dates_time.get_nowutc()
    return response_msg

def latecheckout(user, team=None):
    response_msg = respmsg("Late check out")
    response_msg.add_field(name="User", value=user, inline=False)
    if team:
        response_msg.add_field(name="Team", value=team, inline=False)
    return response_msg

def openscrims(teamlist=None, teamcount=0, latecheckout=False):
    response_msg = respmsg("Scrim signup is open")
    response_msg.add_field(name="Scrim Signup", value="Please remember the latest you can check out is: ```Weekday: 5:30pm AEST\nWeekend: 5:00pm AEST```", inline=False)
    response_msg.add_field(name="Check In", value="```!checkin @team or !checkin```", inline=False)
    response_msg.add_field(name="Check Out", value="```!checkout @team or !checkout```", inline=False)
    response_msg.add_field(name="Team count", value=f"```{teamcount}```", inline=False)
    if teamlist is not None:
        response_msg.add_field(name="Teams:", value=teamlist, inline=False)
    if latecheckout is True:
        response_msg.add_field(name="Check out closed", value="Check outs now will incur a strike!", inline=False)
    return response_msg

def closescrims():
    response_msg = respmsg("Scrim signup is closed")
    response_msg.add_field(name="Sign ups are closed", value="```Please see the lobby channels for team lists```", inline=False)
    return response_msg

def postlobby(teamlist=None, lobbynum=1):
    response_msg = respmsg(f"Lobby {lobbynum}  |  {dates_time.get_today()}")
    response_msg.add_field(name="password", value="```yeet```", inline=False)
    response_msg.add_field(name="Time", value="```Weekday: 5:30pm AEST\nWeekend: 5:00pm AEST```", inline=False)
    if teamlist is not None:
        response_msg.add_field(name="Teams:", value=teamlist, inline=False)
    return response_msg

def cancellobby(teamcount=0):
    response_msg = respmsg(f"Scrims cancelled  |  {dates_time.get_today()}")
    response_msg.add_field(name="Not enough teams", value=f"```{teamcount}```", inline=False)
    return response_msg

def quote():
    request = requests.get("https://leksell.io/zen/api/quotes/random")
    json_data = json.loads(request.text)
    quote = json_data['quote'] + " -" + json_data['author']
    if request.status_code != 200:
        request = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(request.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote

async def send_alert(ctx, header=None, content=None, title="Alert", description=None, permanent=False):
    if description is None:
        notification = discord.Embed(title=title, color=0xD10000)
    else:
        notification = discord.Embed(title=title, description=description, color=0xD10000)
    if not (header is None or content is None):
        notification.add_field(name=header, value=content)
    if not permanent:
        notification.set_footer(text="Message gets deleted in 10 seconds")
        await ctx.message.channel.send(embed=notification, delete_after=10)
    else:
        await ctx.message.channel.send(embed=notification)

async def send_approve(ctx, header=None, content=None, title="Notification", description=None, permanent=False):
    if description is None:
        notification = discord.Embed(title=title, color=0xED321)
    else:
        notification = discord.Embed(title=title, description=description, color=0xED321)
    if not (header is None or content is None):
        notification.add_field(name=header, value=content)
    if not permanent:
        notification.set_footer(text="Message gets deleted in 10 seconds")
        await ctx.message.channel.send(embed=notification, delete_after=10)
    else:
        await ctx.message.channel.send(embed=notification)