from discord.ext import commands
from cakebot.utils.general_utils import send_message


@commands.command(name='join', aliases=['summon'])
async def join(ctx: commands.Context) -> None:
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
        msg = "You are not in a chatroom"
        await send_message(ctx, title="You Are Trash!", msg=msg)


@commands.command(name='leave')
async def leave(ctx: commands.Context) -> None:
    """Leaves voicechannel if possible"""

    try:
        await ctx.voice_client.disconnect()
        await send_message(ctx, title="Bye bitch!")
    except AttributeError:
        await send_message(ctx, title="I'm not in a chatroom loser...")


@commands.command(name='ping')
async def ping(ctx: commands.Context) -> None:
    """Sends the latency of the discord bot"""

    msg = f"Latency is {round(ctx.bot.latency * 1000)}ms"
    await send_message(ctx, title="Pong!", msg=msg)


def setup(bot) -> None:
    commands = [join, leave, ping]
    for command in commands:
        bot.add_command(command)
