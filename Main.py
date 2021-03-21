import os
import discord
import json
import asyncio
import base64

from dotenv import load_dotenv
from replit import db
from keep_alive import keep_alive
from UserInfo import UserInfo
from discord.ext import commands, tasks
from datetime import date, datetime, timedelta, time

#========================================================
# Bot Setup
#========================================================
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_TOKEN')
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='&')

#========================================================
# Global field Setup
#========================================================
pic_ext = ['.png', '.gif', '.jpeg', '.jpg', '.jpeg', '.jpe' ,'.jif', '.jfif', '.jfi']
todaysPosters = []
#========================================================
# Database Functions
#========================================================
def getUser(userKey):
    userJsonFromDB = json.loads(db[userKey])
    return UserInfo(**userJsonFromDB)

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

#========================================================
# Bot Commands
#========================================================

#Send a help message to author
@bot.command(name="howTo")
async def sendHelpPM(ctx):
    author = ctx.author
    header = "DailyPictureBot Help Guide:\n"
    howToUse = "\n    Post a daily Picture in the daily-pictures chat. \n    The bot will track your posting and keep track of your stats.\n    Compete on weekly, monthly and yearly leaderboards.\n    You can only post one picture a day, with the reset happening at midnight every night\n \n"
    commands = "\n    Bot Commands:\n        &howTo - get this reply\n        &me - post your stats\n        &week - show this weeks leaderboard\n        &month - show this months leaderboard\n        &year - show this years leaderboard\n        &total - show the all time leaderboard\n        &streak - get you streak\n        &today - Get the people who have posted today"
    message = header + howToUse + commands
    await author.create_dm()
    await author.dm_channel.send(message)

#Show all info
@bot.command(name="me")
async def showIndividualStats(ctx):
    if ctx.author.name in db.keys():
        userInfo = getUser(ctx.author.name)
        message = "User: {}\nAll-time Posts: {}\nPosts this year: {}\nPosts this month: {}\nPosts this week: {}\nYour streak: {} days".format(userInfo.userName,userInfo.allTime, userInfo.year, userInfo.month, userInfo.week, userInfo.streak)
    else:
        message = "You are yet to post a picture. Now is your chance :smiley:"
    await ctx.send(message)

#Display your current streak
@bot.command(name="streak")
async def showPersonalStreak(ctx):
    if ctx.author.name in db.keys():
        userInfo = getUser(ctx.author.name)
        streak = userInfo.streak

        if streak < 0: #cold streak
            message = "You are on a {} day cold streak 🧊".format(streak)
            await ctx.send(message)
        else:
            message = "You are on a {} day hot streak 🔥".format(streak)
            await ctx.send(message)
    else:
        message = "You are yet to post a picture. Now is your chance :smiley:"
        await ctx.send(message)

#Get people who posted today
@bot.command(name="today")
async def showDailyPosters(ctx):
    postersSoFar = []
    
    keys = db.keys()
    for key in keys:
        userInfo = getUser(key)
        if userInfo.postedToday():
            postersSoFar.append(userInfo.userName)

    message = "Todays posters so far: "
    for user in postersSoFar:
        message += "\n" + str(user)

    await ctx.send(message)


#Get week leaderboard
@bot.command(name="week")
async def showWeeklyRanking(ctx): 
    posters = []

    keys = db.keys()
    for key in keys:
        user = getUser(key)
        posters.append({"User": user.userName, "Week":user.week})
    posters.sort(key=getWeek, reverse=True)
    
    message = "This weeks rankings so far:"
    index = 1;
    for poster in posters:
        message += "\n{}. {} with {}".format(index, poster.get("User"), poster.get("Week"))
        index += 1
    
    await ctx.send(message)

#Get month leaderboard
@bot.command(name="month")
async def showMonthlyRanking(ctx): 
    posters = []
    keys = db.keys()
    for key in keys:
        user = getUser(key)
        posters.append({"User": user.userName, "Month":user.month})
    posters.sort(key=getMonth, reverse=True)

    message = "This months rankings so far:"
    index = 1;
    for poster in posters:
        message += "\n{}. {} with {}".format(index, poster.get("User"), poster.get("Month"))
        index += 1
    await ctx.send(message)

#Get year leaderboard
@bot.command(name="year")
async def showYearlyRanking(ctx): 
    posters = []
    keys = db.keys()
    for key in keys:
        user = getUser(key)
        posters.append({"User": user.userName, "Year":user.year})
    posters.sort(key=getYear, reverse=True)

    message = "This years rankings so far:"
    index = 1;
    for poster in posters:
        message += "\n{}. {} with {}".format(index, poster.get("User"), poster.get("Year"))
        index += 1
    await ctx.send(message)

#Get all time leaderboard
@bot.command(name="total")
async def showAllTimeRanking(ctx): 
    posters = []
    keys = db.keys()
    for key in keys:
        user = getUser(key)
        posters.append({"User": user.userName, "AllTime": user.allTime})
    posters.sort(key=getAllTime, reverse=True)

    message = "All time rankings are:"
    index = 1;
    for poster in posters:
        message += "\n{}. {} with {}".format(index, poster.get("User"), poster.get("AllTime"))
        index += 1
    await ctx.send(message)

#========================================================
# Sorting Helper Functions
#========================================================
def getWeek(user):
    return user.get('Week')

def getMonth(user):
    return user.get('Month')

def getYear(user):
    return user.get('Year')

def getAllTime(user):
    return user.get('AllTime')

#========================================================
# Bot Events
#========================================================
@bot.event
async def on_ready():
    print("Bot is ready")


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to Daily Pics!')


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user or message.channel.id !=  821781619106381874:
        return

    await check_message(message)


#========================================================
# Message Checking functions
#========================================================   

#Check message to see if a picture was posted
async def check_message(message):
    if len(message.attachments) != 1:
        await warn_user_pictures_only(message.author)
        await message.delete()
        return
    
    file = message.attachments[0].filename.lower()

    for ext in pic_ext:
        if file.endswith(ext):
            await handlePicutrePost(message)
            return
    
    await warn_user_ext_only(message.author)
    await message.delete()

# handle a picture post
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
            await changeServerIcon(message)
            await author.create_dm()
            await author.dm_channel.send("Great job! See you again tomorrow :smiley:")
    else:
        userInfo = UserInfo(author.name, int(datetime.now().timestamp()), 0, 0, 0, 0, 0)
        userInfo.addPost()
        userJSON = json.dumps(userInfo.__dict__) 
        db[author.name] = userJSON
        await changeServerIcon(message)
        await author.create_dm()
        await author.dm_channel.send("Great job! See you again tomorrow :smiley:")

# change server icon to new picture (not gifs)
async def changeServerIcon(message):
    file = message.attachments[0].filename.lower()

    icon_ext = ['.png', '.jpeg', '.jpg', '.jpeg', '.jpe' ,'.jif', '.jfif', '.jfi']

    allowFile = False;

    for ext in icon_ext:
        if file.endswith(ext):
            allowFile = True

    if allowFile == False:
        return

    for guild in bot.guilds:
        server = guild
        file = await message.attachments[0].read()
        await server.edit(icon=file)


#========================================================
# Announcements functions
#========================================================
async def announceWeekWinner():
    if len(db.keys()) == 0:
        return

    posters = []
    keys = db.keys()
    for key in keys:
        user = getUser(key)
        posters.append({"User": user.userName, "Week": user.week})
    posters.sort(key=getWeek, reverse=True)

    highestScore = posters[0].get("Week");
    userString = ""


    for poster in posters:
        if poster.get("Week") == highestScore:
            userString += poster.get("User") + " "


    message = "This weeks winner: {} with {} posts! Keep up the good work! 🎉📷🏆".format(userString, posters[0].get("Week"))
    for guild in bot.guilds:
        channel = guild.get_channel(821781619106381874)
        await channel.send(message)

async def announceMonthWinner():
    if len(db.keys()) == 0:
        return

    posters = []
    keys = db.keys()
    for key in keys:
        user = getUser(key)
        posters.append({"User": user.userName, "Month": user.month})
    posters.sort(key=getMonth, reverse=True)

    highestScore = posters[0].get("Month");
    userString = ""
    for poster in posters:
        if poster.get("Month") == highestScore:
            userString += poster.get("User") + " "

    message = "This months winner: {} with {} posts! Well done!🎉🎉📷🖼️🏆🏆".format(userString, posters[0].get("Month"))
    for guild in bot.guilds:
        channel = guild.get_channel(821781619106381874)
        await channel.send(message)

async def announceYearWinner():
    if len(db.keys()) == 0:
        return
        
    posters = []
    keys = db.keys()
    for key in keys:
        user = getUser(key)
        posters.append({"User": user.userName, "Year": user.year})
    posters.sort(key=getYear, reverse=True)

    highestScore = posters[0].get("Year");
    userString = ""
    for poster in posters:
        if poster.get("Year") == highestScore:
            userString += poster.get("User") + " "

    message = "This years winner: {} with {} posts! Great job!!! 🎉🎉🎉📷🖼️🏆🏆🏆".format(userString, posters[0].get("Year"))
    for guild in bot.guilds:
        channel = guild.get_channel(821781619106381874)
        await channel.send(message)

#========================================================
# Warning functions
#========================================================
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

#========================================================
# Repeating Background functions
#========================================================
@tasks.loop(hours=24)
async def called_once_a_day():
    keys = db.keys()
    for key in keys:
        userInfo = getUser(key)
        if userInfo.postedToday():
            todaysPosters.append(userInfo.userName)
        userInfo.dailyCheck()
        print("Checked: " + userInfo.userName)
        userJSON = json.dumps(userInfo.__dict__)
        db[key] = userJSON
    await announceDailyPosters()
    await checkLeaderboardReset()
    print("Reset Daily Stats")
        

@called_once_a_day.before_loop
async def before():
    now = datetime.now()
    midnight = datetime.combine(now + timedelta(days=1), time())
    secondsUntilMidnight = (midnight - now).seconds
    await asyncio.sleep(secondsUntilMidnight)
    print("Finished waiting")

async def checkLeaderboardReset():
    now = date.today()
    if checkIfFirstDayOfWeek():
        await announceWeekWinner()
        await clearWeeklyLeaderBoard()
    if checkIfFirstDayOfMonth(now):
        await announceMonthWinner()
        await clearMonthlyLeaderBoard()
    if checkIfFirstDayOfyear(now):
        await announceYearWinner()
        await clearYearlyLeaderBoard()

async def announceDailyPosters():
    message = "Todays posters: "
    for user in todaysPosters:
        message += "\n" + str(user)
    
    channel = bot.get_channel(821781619106381874)
    await channel.send(message)
    todaysPosters.clear()

#========================================================
# Reset LeaderBoard Events
#========================================================
async def clearWeeklyLeaderBoard():
    keys = db.keys()
    for key in keys:
        user = getUser(key)
        user.resetWeeklyStats()


async def clearMonthlyLeaderBoard():
    keys = db.keys()
    for key in keys:
        user = getUser(key)
        user.resetMonthlyStats()

async def clearYearlyLeaderBoard():
    keys = db.keys()
    for key in keys:
        user = getUser(key)
        user.resetYearlyStats()

#========================================================
# Date Event Checkers
#========================================================
def checkIfFirstDayOfWeek():
    if date.today().weekday() == 0:
        print("New Week")
        return True
    return False


def checkIfFirstDayOfMonth(date):
    if date.day == 1:
        print("New Month")
        return True
    return False

def checkIfFirstDayOfyear(date):
    if date.day == 1 and date.month == 1:
        print("New Year")
        return True
    return False


called_once_a_day.start()
keep_alive()
bot.run(TOKEN)