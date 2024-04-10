import os

import disnake
from disnake.ext import commands
from dotenv import load_dotenv, find_dotenv
from config import guild
from database import VoiceDb
from load import load

load_dotenv(find_dotenv())
token = os.getenv("TOKEN")


bot = commands.Bot(command_prefix='!',
                   intents=disnake.Intents.all(),
                   activity=disnake.Game("VS code"),
                   status=disnake.Status.online,
                   test_guilds=guild)


@bot.event
async def on_ready():
    this_guild = bot.get_guild(guild[0])
    await load(bot).create_channels(this_guild)
    await VoiceDb().crate_table()


for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f"cogs.{file[:-3]}")

bot.run(token)
