import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='join')
    async def join(self, ctx: commands.Context) -> None:
        """Joins the authors voice channel."""

        author = ctx.author.voice
        if author:
            destination = author.channel
            bot_location = ctx.voice_client

            if bot_location:
                await bot_location.move_to(destination)
            else:
                await destination.connect()
        else:
            await ctx.send(content="You are not in a chatroom :cake:")

    @commands.command(name="leave")
    async def _leave(self, ctx: commands.Context) -> None:
        try:
            await ctx.voice_client.disconnect()
        except:
            await ctx.send(content="I'm not connected :cake:")

def setup(bot) -> None:
    bot.add_cog(General(bot))