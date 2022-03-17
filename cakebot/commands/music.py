import discord
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='play')
    async def _play(ctx, self) -> None:
        pass

    @commands.command(name='skip')
    async def _skip(ctx, self):
        pass

def setup(bot):
    bot.add_cog(Music(bot))
