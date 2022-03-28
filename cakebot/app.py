import discord
from discord.ext import commands

import logging
import os
from dotenv import load_dotenv


def main() -> None:
    """Starts discord bot with logging in terminal"""

    logging.basicConfig(level=logging.INFO)
    load_dotenv() # Get access to .env
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    
    bot = commands.Bot(command_prefix='!')
    
    extensions = ['commands.general', 'commands.music']
    for extension in extensions: bot.load_extension(extension)

    bot.run(DISCORD_TOKEN)


if __name__ == '__main__':
    main()
