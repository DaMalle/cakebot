from discord.ext import commands

from cakebot.utils.general_utils import send_message
from cakebot.utils import music_utils
from cakebot.commands.general import join

class Music(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.music_player = music_utils.MusicPlayer()
        
    @commands.command(name='play')
    async def _play(self, ctx, *song_request) -> None:
        await join(ctx)
        
        if ctx.author.voice.channel == ctx.voice_client.channel:
            await self.music_player.add(ctx, ' '.join(song_request))
            if not ctx.voice_client.is_playing():
                await self.music_player.play(ctx)

    @commands.command(name='skip')
    async def _skip(self, ctx) -> None:
        ctx.voice_client.stop()
        await self.music_player.play(ctx)

    @commands.command(name='pause')
    async def _pause(self, ctx) -> None:
        ctx.voice_client.pause()

    @commands.command(name='resume')
    async def _resume(self, ctx) -> None:
        ctx.voice_client.resume()

    @commands.command(name='clear')
    async def _clear(self, ctx) -> None:
        self.music_player.clear_queue()

    @commands.command(name='stop')
    async def _stop(self, ctx) -> None:
        self.music_player.clear_queue()
        ctx.voice_client.stop()

    @commands.command(name='queue')
    async def _queue(self, ctx) -> None:
        await send_message(ctx, title="The queue is:",
                           msg=self.music_player.get_queue())

def setup(bot):
    bot.add_cog(Music(bot))
