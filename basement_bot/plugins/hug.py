import random

import cogs
import decorate
import discord
from discord.ext import commands


def setup(bot):
    bot.add_cog(Hugger(bot))


class Hugger(cogs.BasicPlugin):

    PLUGIN_NAME = __name__
    HAS_CONFIG = False

    HUGS_SELECTION = [
        "{user_giving_hug} hugs {user_to_hug} forever and ever and ever",
        "{user_giving_hug} wraps arms around {user_to_hug} and clings forever",
        "{user_giving_hug} hugs {user_to_hug} and gives their hair a sniff",
        "{user_giving_hug} glomps {user_to_hug}",
        "cant stop, wont stop. {user_giving_hug} hugs {user_to_hug} until the sun goes cold",
        "{user_giving_hug} reluctantly hugs {user_to_hug}...",
        "{user_giving_hug} hugs {user_to_hug} into a coma",
        "{user_giving_hug} smothers {user_to_hug} with a loving hug",
        "{user_giving_hug} squeezes {user_to_hug} to death",
    ]
    ICON_URL = (
        "https://cdn.icon-icons.com/icons2/1648/PNG/512/10022huggingface_110042.png"
    )

    @decorate.with_typing
    @commands.has_permissions(send_messages=True)
    @commands.command(
        name="hug",
        brief="Hugs a user",
        description="Hugs a mentioned user using an embed",
        usage="@user",
    )
    async def hug(self, ctx, user_to_hug: discord.Member):
        """Executes the hug command. Returns bot's response

        parameters:
            ctx (Context): the context
        """
        if user_to_hug.id == ctx.author.id:
            await self.bot.h.tagged_response(ctx, "Let's be serious")
            return

        embed = self.generate_embed(ctx, user_to_hug)

        await self.bot.h.tagged_response(ctx, embed=embed, target=user_to_hug)

    def generate_embed(self, ctx, user_to_hug):
        hug_text = random.choice(self.HUGS_SELECTION).format(
            user_giving_hug=ctx.author.mention,
            user_to_hug=user_to_hug,
        )

        embed = self.bot.embed_api.Embed()

        embed.add_field(name="You've been hugged!", value=hug_text)

        embed.set_thumbnail(url=self.ICON_URL)

        return embed
