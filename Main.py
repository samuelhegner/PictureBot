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

def update_user(user_name):
    pass
    



@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(f'{client.user} is connected to the following guild:\n'
          f'{guild.name}(id: {guild.id})')

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to Daily Pics!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return


keep_alive()
client.run(TOKEN)
