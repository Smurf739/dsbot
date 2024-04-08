import os

import disnake
from disnake.ext import commands
from dotenv import load_dotenv, find_dotenv
from config import guild

load_dotenv(find_dotenv())
token = os.getenv("TOKEN")

bot = commands.Bot(command_prefix='!',
                   intents=disnake.Intents.all(),
                   activity=disnake.Game("VS code"),
                   status=disnake.Status.online,
                   test_guilds=guild)


for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f"cogs.{file[:-3]}")

bot.run(token)
