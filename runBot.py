import discord, datetime, time, sqlite3, os
from cardAssets import createCard
from discord import NotFound
from discord.utils import get

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
    db_connection.close()

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

    # -----------------------------------------------------------   
    #                      View Karma Command
    # -----------------------------------------------------------
	
    if usermessage.startswith("$karma"):
        usermessage = usermessage.split(" ")
        db_connection = sqlite3.connect('user_data.db')
        db_c = db_connection.cursor()

        if len(usermessage) == 2:
            user_id_to_use = int(usermessage[1].replace("<@","").replace(">","").replace("!",""))
            member = message.guild.get_member(user_id_to_use)
            username_to_use = member.name
            avatar = member.avatar_url
        
        else:
            user_id_to_use = message.author.id
            username_to_use = message.author.name

        try:
            db_c.execute("SELECT * FROM userdata WHERE userid=?", (user_id_to_use,))
            individual_user_data = db_c.fetchall()
            individual_user_data = str(individual_user_data[0]).replace("(","").replace(")","").replace(" ","").split(",")
        except:
            individual_user_data = [user_id_to_use,0,0]

        createCard.createCard(individual_user_data[1],individual_user_data[2],username_to_use,avatar)
        await message.channel.send(file = discord.File("card.png"))
			
@client.event
async def on_raw_reaction_add(payload):
    upvote,downvote = 0,0
    if payload.emoji.id == upvote_emoji:
        upvote = 1
    elif payload.emoji.id == downvote_emoji:
        downvote = 1
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


    if payload.user_id == msg.author.id:
        return

    db_connection = sqlite3.connect('user_data.db')
    db_c = db_connection.cursor()

    db_c.execute("SELECT * FROM userdata WHERE userid=?", (msg.author.id,))
    individual_user_data = db_c.fetchall()

    if individual_user_data == []: #if user doesnt exist in db
        sqlite_insert_with_param = """INSERT INTO userdata
                          (userid, upvotes, downvotes) 
                          VALUES (?, ?, ?);"""
        data_tuple = (msg.author.id,upvote,downvote)
        db_c.execute(sqlite_insert_with_param, data_tuple)
        db_connection.commit()
        db_connection.close()
        return
    else:
        individual_user_data = str(individual_user_data[0]).replace("(","").replace(")","").replace(" ","").split(",")
        
        db_c.execute("DELETE from userdata where userid = ?",(msg.author.id,))
        sqlite_insert_with_param = """INSERT INTO userdata
                            (userid, upvotes, downvotes) 
                            VALUES (?, ?, ?);"""

        upvotes = int(individual_user_data[1])+upvote
        downvotes = int(individual_user_data[2])+downvote
        data_tuple = (msg.author.id,upvotes,downvotes)
        db_c.execute(sqlite_insert_with_param, data_tuple)
        db_connection.commit()
        db_connection.close()

@client.event
async def on_raw_reaction_remove(payload):
    upvote,downvote = 0,0
    if payload.emoji.id == upvote_emoji:
        upvote = 1
    elif payload.emoji.id == downvote_emoji:
        downvote = 1
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

    if payload.user_id == msg.author.id:
        return

    db_connection = sqlite3.connect('user_data.db')
    db_c = db_connection.cursor()

    db_c.execute("SELECT * FROM userdata WHERE userid=?", (msg.author.id,))
    individual_user_data = db_c.fetchall()

    if individual_user_data == []:
        print("No user data to remove reaction from")
        return

    else:
        individual_user_data = str(individual_user_data[0]).replace("(","").replace(")","").replace(" ","").split(",")
        
        db_c.execute("DELETE from userdata where userid = ?",(msg.author.id,))
        sqlite_insert_with_param = """INSERT INTO userdata
                            (userid, upvotes, downvotes) 
                            VALUES (?, ?, ?);"""

        upvotes = int(individual_user_data[1])-upvote
        downvotes = int(individual_user_data[2])-downvote
        data_tuple = (msg.author.id,upvotes,downvotes)
        db_c.execute(sqlite_insert_with_param, data_tuple)
        db_connection.commit()
        db_connection.close()

client.run(discordKey)