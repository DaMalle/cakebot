import youtube_dl
import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

def main():
    load_dotenv() # Get access to .env
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    
    #intents = discord.Intents().all()
    #client = discord.Client(intents=intents)
    bot = commands.Bot(command_prefix='!') #, intents=intents)

    bot.load_extension('commands.general')
    bot.load_extension('commands.music')
    bot.run(DISCORD_TOKEN)

if __name__ == '__main__':
    main()