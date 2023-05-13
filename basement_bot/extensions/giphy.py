import base
import util
from discord.ext import commands


async def setup(bot):
    await bot.add_cog(Giphy(bot=bot))


class Giphy(base.BaseCog):

    GIPHY_URL = "http://api.giphy.com/v1/gifs/search?q={}&api_key={}&limit={}"
    SEARCH_LIMIT = 10

    @staticmethod
    def parse_url(url):
        index = url.find("?cid=")
        return url[:index]

    @util.with_typing
    @commands.guild_only()
    @commands.command(
        name="giphy",
        brief="Grabs a random Giphy image",
        description="Grabs a random Giphy image based on your search",
        usage="[query]",
    )
    async def giphy(self, ctx, *, query: str):
        response = await self.bot.http_call(
            "get",
            self.GIPHY_URL.format(
                query.replace(" ", "+"),
                self.bot.file_config.main.api_keys.giphy,
                self.SEARCH_LIMIT,
            ),
        )

        data = response.get("data")
        if not data:
            await ctx.send_deny_embed(f"No search results found for: *{query}*")
            return

        embeds = []
        for item in data:
            url = item.get("images", {}).get("original", {}).get("url")
            url = self.parse_url(url)
            embeds.append(url)

        ctx.task_paginate(pages=embeds)
