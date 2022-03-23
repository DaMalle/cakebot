
import discord
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands
from discord.utils import get
from yt_dlp import YoutubeDL

from cakebot.utils import music_utils
from cakebot.commands.general import General

class Music(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.mp = music_utils.MusicPlayer()

        self.ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
            'options': '-vn'
        }
        

    @commands.command(name='play')
    async def _play(self, ctx) -> None:
        await self.bot.get_cog('General').join(ctx)
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        self.mp.current_song = await self._get_song_info(ctx)
        print(self.mp.current_song)
        voice.play(FFmpegPCMAudio(self.mp.current_song, **self.ffmpeg_options), after=lambda e: print("test"))
        

    @commands.command(name='skip')
    async def _skip(self, ctx) -> None:
        pass

    async def _get_song_info(self, ctx) -> dict:
        song = "https://www.youtube.com/watch?v=kJQP7kiw5Fk"
        downloader = YoutubeDL({'title': True})
        r = downloader.extract_info(song, download=False)
        return r.get('url')

def setup(bot):
    bot.add_cog(Music(bot))