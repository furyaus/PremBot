from utils import notification

def role_mentioned(ctx):
    if len(ctx.message.role_mentions) != 0:
        return True
    else:
        message = "No role mentioned"
        print(message)
        notification.send_alert(ctx=ctx, header=message, content="")
        return False

def is_numeric(message):
    return message.content.isnumeric()