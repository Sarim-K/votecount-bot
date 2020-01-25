import discord, datetime, time, sqlite3, os
from discord import NotFound

def opencfg(filename):
    file = open(filename,"r")
    keys = file.readlines()
    
    keyList = []
    for entry in keys:
        tempEntry = entry.split("=")
        tempEntry = tempEntry[1]
        tempEntry = tempEntry.replace(" ","")
        tempEntry = tempEntry.strip()
        keyList.append(tempEntry)
    return keyList
keyList = opencfg("apikeys.txt")
API_KEY, discordKey, testDiscordKey, GENIUS_API_KEY = str(keyList[0]), str(keyList[1]), str(keyList[2]), str(keyList[3])
upvote_emoji = 452121917462151169
downvote_emoji = 451890347761467402

try:
    db_connection = sqlite3.connect('file:user_data.db?mode=rw', uri=True) #uri raises exception if db doesn't exist
    #db_cursor = db_connection.cursor() ##############

except sqlite3.OperationalError:
    print("Database does not exist, creating database.")
    db_connection = sqlite3.connect('user_data.db')
    db_c = db_connection.cursor()

    db_c.execute("""CREATE TABLE userdata (
                    userid integer,
                    upvotes integer,
                    downvotes integer
                )""")
    db_connection.commit()
    db_connection.close()

except Exception as e:
    print(f"Unknown error.\n{e}")

client = discord.Client()
@client.event
async def on_ready():
    print("logged in as {0.user}".format(client))
    
@client.event
async def on_message(message):
    usermessage = message.content.lower()
    avatar = str(message.author.avatar_url)
    avatar = avatar.replace("webp?size=1024","png?size=32")
    discordname = str(message.author.name)+"#"+str(message.author.discriminator)

    # -----------------------------------------------------------   
    #                        First Command
    # -----------------------------------------------------------
	
    if usermessage.startswith("$firstcmd"):
        title,description,colour=None,None,None
        embed = discord.Embed(title=title,description=description,color=colour)
        embed.set_author(name=discordname, icon_url=avatar)
        await message.channel.send(embed=embed)
			
@client.event
async def on_raw_reaction_add(payload):
    if payload.emoji.id == upvote_emoji:
        vote = "upvote"
    elif payload.emoji.id == downvote_emoji:
        vote = "downvote"
    else:
        return

    channel = client.get_channel(payload.channel_id)
    try:
        msg = await channel.fetch_message(payload.message_id)
    except NotFound:
        print("Message not found.")
        return
    except Exception as e:
        print(f"Unknown error.\n{e}")

    db_connection = sqlite3.connect('user_data.db')
    db_c = db_connection.cursor()

    db_c.execute("SELECT * FROM userdata WHERE userid=?", (msg.author.id,))
    individual_user_data = db_c.fetchall()
    print(individual_user_data)
    print(type(individual_user_data))

    if vote == "upvote":
        print()
        ### https://pynative.com/python-sqlite-insert-into-table/

    db_connection.commit()
    db_connection.close()

    print(msg.author.id)

client.run(discordKey)
