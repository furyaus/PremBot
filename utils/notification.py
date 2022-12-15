import discord, json, requests
from utils import dates_time

def respmsg(titleText=None, descText=None):
    if (titleText == None and descText == None):
        response_msg = discord.Embed(colour=discord.Colour.green())
    if (titleText != None and descText == None):
        response_msg = discord.Embed(colour=discord.Colour.green(),title=titleText)
    if (titleText == None and descText != None):
        response_msg = discord.Embed(colour=discord.Colour.green(),description=descText)
    if (titleText != None and descText != None):
        response_msg = discord.Embed(colour=discord.Colour.green(),title=titleText,description=descText)
    response_msg.set_thumbnail(url="https://i.ibb.co/GCTgdsz/premlogo-100px.png")
    return response_msg

def printcon(content):
    print(f"{dates_time.get_now()} | "+content)
 
def quote():
    request = requests.get("https://leksell.io/zen/api/quotes/random")
    json_data = json.loads(request.text)
    quote = json_data['quote'] + " -" + json_data['author']
    if request.status_code != 200:
        request = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(request.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote

async def send_alert(ctx, header=None, content=None, title="Notification", description=None, permanent=False):
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
