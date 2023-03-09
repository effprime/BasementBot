import base
import discord
import util
from discord.ext import commands


async def setup(bot):
    await bot.add_cog(Wolfram(bot=bot))


class WolframEmbed(discord.Embed):

    ICON_URL = "https://cdn.icon-icons.com/icons2/2107/PNG/512/file_type_wolfram_icon_130071.png"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = discord.Color.orange()
        self.set_thumbnail(url=self.ICON_URL)


class Wolfram(base.BaseCog):

    API_URL = "http://api.wolframalpha.com/v1/result?appid={}&i={}"

    @util.with_typing
    @commands.cooldown(3, 60, commands.BucketType.channel)
    @commands.command(
        name="wa",
        aliases=["math", "wolframalpha", "jarvis"],
        brief="Searches Wolfram Alpha",
        description="Searches the simple answer Wolfram Alpha API",
        usage="[query]",
    )
    async def simple_search(self, ctx, *, query: str):
        url = self.API_URL.format(
            self.bot.file_config.main.api_keys.wolfram,
            query,
        )

        response = await self.bot.http_call("get", url, get_raw_response=True)
        if response.status == 501:
            await ctx.send_deny_embed("Wolfram|Alpha did not like that question")
            return
        if response.status != 200:
            await ctx.send_deny_embed(f"Wolfram|Alpha ran into an error")
            return

        answer = await response.text()
        await ctx.send(embed=WolframEmbed(description=answer))
