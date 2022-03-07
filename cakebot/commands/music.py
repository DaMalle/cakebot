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
        #Get channel from author
        channel = ctx.author.voice.channel


    @commands.command(name='leave')
    async def _leave(ctx, self) -> None:
        pass

    #Hukket fra stack # stonks!
    def is_connected(ctx):
        pass
        #voice_client = get(ctx.bot.voice_clients, guild = ctx.guild)
        #return voice_client and voice_client.is_connected()

def setup(bot):
    bot.add_cog(Music(bot))