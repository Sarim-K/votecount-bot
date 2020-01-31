import discord

class createHelpMessage:
    def __init__(self, title, description, colour):
        self.title = title
        self.description = description
        self.colour = colour

def helpcommands(usermessage,message,avatar,admin):
    
    if usermessage == "$help blacklist": #admin only
        if admin == True:
            help_message = createHelpMessage("blacklist a user from being recognised from the bot:","commands:\n$blacklist add\n$blacklist remove\n$blacklist view",1)
            embed = discord.Embed(title=help_message.title,description=help_message.description,color=help_message.colour)
            embed.set_author(name=message.author, icon_url=avatar)
            return embed
        else:
            return

    elif usermessage == "$help set_karma": #admin only
        if admin == True:
            help_message = createHelpMessage("set a user's upvotes|downvotes:","usage: $set_karma @sarim 20|25",1)
            embed = discord.Embed(title=help_message.title,description=help_message.description,color=help_message.colour)
            embed.set_author(name=message.author, icon_url=avatar)
            return embed
        else:
            return

    elif usermessage == "$help karma":
        help_message = createHelpMessage("displays a user's karma count","",1)
        embed = discord.Embed(title=help_message.title,description=help_message.description,color=help_message.colour)
        embed.set_author(name=message.author, icon_url=avatar)
        return embed

    elif usermessage == "$help": #catch-all help command
        if admin == True:
            help_message = createHelpMessage("karma commands:","$karma\n$set_karma\n$blacklist",1)
        else:
            help_message = createHelpMessage("karma commands:","$karma",1)
        embed = discord.Embed(title=help_message.title,description=help_message.description,color=help_message.colour)
        embed.set_author(name=message.author, icon_url=avatar)
        return embed

    else:
        return

