from discord.ext import commands

from cakebot.utils import music_utils
from cakebot.commands.general import General

class Music(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.music_player = music_utils.MusicPlayer()
        
    @commands.command(name='play')
    async def _play(self, ctx, song_url) -> None:
        await self.bot.get_cog('General').join(ctx)
        self.music_player.add(song_url)
        if not ctx.voice_client.is_playing():
            self.music_player.play(ctx.voice_client)

    @commands.command(name='skip')
    async def _skip(self, ctx) -> None:
        ctx.voice_client.stop()
        self.music_player.play_next(ctx.voice_client)

    @commands.command(name='pause')
    async def _pause(self, ctx) -> None:
        ctx.voice_client.pause()

    @commands.command(name='resume')
    async def _resume(self, ctx) -> None:
        ctx.voice_client.resume()

    @commands.command(name='clear')
    async def _clear(self, ctx) -> None:
        self.music_player.clear_queue()
        ctx.voice_client.stop()

def setup(bot):
    bot.add_cog(Music(bot))
