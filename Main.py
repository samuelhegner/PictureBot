# bot.py
import os
import discord
from replit import db

from keep_alive import keep_alive
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# if "user_name" in db.keys(): check if key exists
# users = db["users"] get the values at the key
# users.append(info) add info to the key
# db[]


pic_ext = ['.jpg','.png','.jpeg', '.gif']


def update_user(user_name):
    pass



@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to Daily Pics!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(message.channel)

    await check_message(message)
        


async def check_message(message):
    if len(message.attachments) != 1:
        await warn_user_pictures_only(message.author)
        await message.delete()
    
    file = message.attachments[0].filename

    for ext in pic_ext:
        if file.endswith(ext):
            await handlePicutrePost(message.author)
            return
    
    await warn_user_ext_only(message.author)
    await message.delete()

async def handlePicutrePost(author):
    pass

async def warn_user_pictures_only(author):
    await author.create_dm()
    await author.dm_channel.send("Please post pictures only!")


async def warn_user_ext_only(author):
    await author.create_dm()
    message = "Please post pictures with the extensions: "
    for ext in pic_ext:
        message += ext + ", "
    
    message += "only!"

    await author.dm_channel.send(message)

keep_alive()
client.run(TOKEN)
