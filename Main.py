# bot.py
import os
import discord
import json
import asyncio

from dotenv import load_dotenv
from replit import db
from keep_alive import keep_alive
from UserInfo import UserInfo
from discord.ext import commands, tasks
from datetime import datetime, timedelta, time






#-----------------------------------------------------------
#db.__delitem__("TestUser")
#
#Get item from DB into UserInfo obj
#-----------------------------------------------------------
#if "TestUser" in db.keys():
#    print("Test User Found!")
#    userJson = json.loads(db["TestUser"])
#    testUser = UserInfo(**userJson)
#    testUser.printUserInfo()
#
#Create and assign UserInfo obj to DB
#------------------------------------------------------------
#else:
#    print("No Test User Found!")
#    testUser = UserInfo("TestUser", int(time.time()), 0, 0, 0, 0, 0)
#    userJSON = json.dumps(testUser.__dict__)
#    db[testUser.userName] = userJSON;

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

pic_ext = ['.jpg','.png','.jpeg', '.gif']



@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to Daily Pics!')


@client.event
async def on_message(message):
    
    if message.author == client.user or message.channel.id !=  821781619106381874:
        return

    await check_message(message)
        


async def check_message(message):
    if len(message.attachments) != 1:
        await warn_user_pictures_only(message.author)
        await message.delete()
        return
    
    file = message.attachments[0].filename

    for ext in pic_ext:
        if file.endswith(ext):
            await handlePicutrePost(message)
            return
    
    await warn_user_ext_only(message.author)
    await message.delete()

async def handlePicutrePost(message):
    author = message.author

    if author.name in db.keys():
        userJsonFromDB = json.loads(db[author.name])
        userInfo = UserInfo(**userJsonFromDB)
        print(userInfo.postedToday())
        if (userInfo.postedToday() == True):
            await warn_user_daily_post(message.author)
            await message.delete()
        else:
            userInfo.addPost()
            userJSON = json.dumps(userInfo.__dict__)
            db[author.name] = userJSON
            print(userJSON)  
    else:
        userInfo = UserInfo(author.name, int(time.time()), 0, 0, 0, 0, 0)
        userInfo.addPost()
        userJSON = json.dumps(userInfo.__dict__) 
        db[author.name] = userJSON
        print(userJSON)
        await author.create_dm()
        await author.dm_channel.send("Great job! See you again tomorrow :smiley:")


async def warn_user_pictures_only(author):
    await author.create_dm()
    await author.dm_channel.send("Please post pictures only!")


async def warn_user_daily_post(author):
    await author.create_dm()
    await author.dm_channel.send("Please post only one picture a day!")


async def warn_user_ext_only(author):
    await author.create_dm()
    message = "Please post pictures with the extensions: "
    for ext in pic_ext:
        message += ext + ", "
    message += "only!"
    await author.dm_channel.send(message)

@tasks.loop(minutes=1)
async def called_once_a_day():
    keys = db.keys()
    for key in keys:
        userJsonFromDB = json.loads(db[key])
        userInfo = UserInfo(**userJsonFromDB)
        userInfo.dailyCheck()
        print("Checked: " + userInfo.userName)
        userJSON = json.dumps(userInfo.__dict__)
        db[key] = userJSON
    print("Reset Daily Stats")
        

@called_once_a_day.before_loop
async def before():
    now = datetime.now()
    midnight = datetime.combine(now + timedelta(days=1), time())
    secondsUntilMidnight = (midnight - now).seconds
    await asyncio.sleep(secondsUntilMidnight)
    print("Finished waiting")


def clearDB():
    keys = db.keys()
    for key in keys:
        del db[key]
        

def printDB():
    print("-----------------------------------------------------")
    keys = db.keys()
    for key in keys:
        userJsonFromDB = json.loads(db[key])
        userInfo = UserInfo(**userJsonFromDB)
        userInfo.printUserInfo()
        print("-----------------------------------------------------")

called_once_a_day.start()
keep_alive()
client.run(TOKEN)



