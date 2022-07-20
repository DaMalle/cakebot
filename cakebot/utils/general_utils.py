from discord import Embed, Colour


async def send_message(ctx, title: str = "", msg: str = "") -> None:
    await ctx.send(embed=Embed(
        colour=Colour.red(), title=title, description=msg))
