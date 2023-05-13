import random

import base
import discord
import util
from discord.ext import commands


async def setup(bot):
    await bot.add_cog(Burn(bot=bot))


class BurnEmbed(discord.Embed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = "Burn Alert!"
        self.color = discord.Color.red()


class Burn(base.BaseCog):
    SEARCH_LIMIT = 50
    PHRASES = [
        "Sick BURN!",
        "Someone is going to need ointment for that BURN!",
        "Fire! Call 911! Someone just got BURNED!",
        "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOH BURN!",
        "BURN ALERT!",
        "Was that message a hot pan? BECAUSE IT BURNS!",
    ]

    @commands.guild_only()
    @commands.command(
        brief="Declares a BURN!",
        description="Declares the user's last message as a BURN!",
        usage="@user",
    )
    async def burn(self, ctx, user_to_match: discord.Member):
        matched_message = None

        prefix = await self.bot.get_prefix(ctx.message)

        async for message in ctx.channel.history(limit=self.SEARCH_LIMIT):
            if message.author == user_to_match and not message.content.startswith(
                prefix
            ):
                matched_message = message
                break

        if not matched_message:
            await ctx.send_deny_embed("I could not a find a message to reply to")
            return

        for emoji in ["🔥", "🚒", "👨‍🚒"]:
            await matched_message.add_reaction(emoji)

        message = random.choice(self.PHRASES)
        embed = BurnEmbed(description=f"🔥🔥🔥 {message} 🔥🔥🔥")
        await ctx.send(embed=embed, targets=[user_to_match])
