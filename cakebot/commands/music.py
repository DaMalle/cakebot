from discord.ext import commands

from cakebot.utils import music_utils
from cakebot.commands.general import General

class Music(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.mp = music_utils.MusicPlayer()
        
    @commands.command(name='play')
    async def _play(self, ctx, song_url) -> None:
        await self.bot.get_cog('General').join(ctx)
        self.mp.add(song_url)
        voice_client = ctx.voice_client
        if not voice_client.is_playing():
            self.mp.play(voice_client)

    @commands.command(name='skip')
    async def _skip(self, ctx) -> None:
        ctx.voice_client.stop()

    @commands.command(name='pause')
    async def _pause(self, ctx) -> None:
        ctx.voice_client.pause()

    @commands.command(name='resume')
    async def _resume(self, ctx) -> None:
        ctx.voice_client.resume()

def setup(bot):
    bot.add_cog(Music(bot))
