# bot.py
import os
import discord
import pandas as pd

from dotenv import load_dotenv

try:
    dataframe = pd.read_csv("./data.csv")

except FileNotFoundError:
    dataframe = pd.DataFrame({'User': pd.Series([], dtype='str'),
                              'Last Post': pd.Series([], dtype='str'),
                              'Hot Streak': pd.Series([], dtype='int'),
                              'Weekly Count': pd.Series([], dtype='int'),
                              'Monthly Count': pd.Series([], dtype='int'),
                              'All Time': pd.Series([], dtype='int')})

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to Daily Pics!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    current = pd.DataFrame.copy(dataframe)
    user_name = message.author._user.name
    user_exists = dataframe['User'].str.contains(user_name)
    if not user_exists.empty:
        row = dataframe.loc[dataframe['User'] == user_name]
        dataframe.set_value('All Time', row.index, row['All Time'] + 1)
    else:
        row = pd.DataFrame([{'User': user_name, 'Last Post': 'butts', 'Hot Streak': 1, 'Weekly Count': 1,
                            'Monthly Count': 1,
                            'All Time': 1}])
        with pd.option_context('display.max_rows', None, 'display.max_columns',
                               None):  # more options can be specified also
            print(current)
        current = dataframe.append(row)

    with pd.option_context('display.max_rows', None, 'display.max_columns',
                           None):  # more options can be specified also
        print(current)
    current.to_csv("data.csv", sep=',')

client.run(TOKEN)