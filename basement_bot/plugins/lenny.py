from discord.ext import commands
from random import choice


def setup(bot):
    bot.add_command(lenny)


@commands.command(name="len")
async def lenny(ctx):
    await ctx.send(choice(lennys))


lennys = [
    "( ͡° ͜ʖ ͡°)",
    "( ͠° ͟ʖ ͡°)",
    "( ͡ʘ ͜ʖ ͡ʘ)",
    "(° ͜ʖ °)",
    "ಠ_ಠ",
    "( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)",
    "༼  ͡° ͜ʖ ͡° ༽",
    "(͡ ͡° ͜ つ ͡͡°)",
    "[̲̅$̲̅(̲̅ ͡° ͜ʖ ͡°̲̅)̲̅$̲̅]",
]
