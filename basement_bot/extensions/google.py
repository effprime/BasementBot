import base
import discord
import util
from discord.ext import commands


def setup(bot):
    config = bot.ExtensionConfig()
    config.add(
        key="max_responses",
        datatype="int",
        title="Max Responses",
        description="The max amount of responses per embed page",
        default=1,
    )

    bot.add_cog(Googler(bot=bot))
    bot.add_extension_config("google", config)


class Googler(base.BaseCog):

    GOOGLE_URL = "https://www.googleapis.com/customsearch/v1"
    YOUTUBE_URL = "https://www.googleapis.com/youtube/v3/search?part=id&maxResults=1"

    async def get_items(self, url, data):
        response = await util.http_call("get", url, params=data)
        return response.get("items")

    @commands.group(
        aliases=["g"],
        brief="Executes a Google command",
        description="Executes a Google command",
    )
    async def google(self, ctx):
        pass

    @util.with_typing
    @commands.has_permissions(send_messages=True)
    @commands.guild_only()
    @google.command(
        aliases=["s"],
        brief="Searches Google",
        description="Returns the top Google search result",
        usage="[query]",
    )
    async def search(self, ctx, *, query: str):
        data = {
            "cx": self.bot.file_config.main.api_keys.google_cse,
            "q": query,
            "key": self.bot.file_config.main.api_keys.google,
        }

        items = await self.get_items(self.GOOGLE_URL, data)

        if not items:
            await util.send_with_mention(ctx, f"No search results found for: *{query}*")
            return

        config = await self.bot.get_context_config(guild=ctx.guild)

        embed = None
        embeds = []
        if not getattr(ctx, "image_search", None):
            field_counter = 1
            for index, item in enumerate(items):
                link = item.get("link")
                snippet = item.get("snippet", "<Details Unknown>").replace("\n", "")
                embed = (
                    discord.Embed(
                        title=f"Results for {query}", value="https://google.com"
                    )
                    if field_counter == 1
                    else embed
                )
                embed.add_field(name=link, value=snippet, inline=False)
                if (
                    field_counter == config.extensions.google.max_responses.value
                    or index == len(items) - 1
                ):
                    embed.set_thumbnail(
                        url="https://cdn.icon-icons.com/icons2/673/PNG/512/Google_icon-icons.com_60497.png"
                    )
                    embeds.append(embed)
                    field_counter = 1
                else:
                    field_counter += 1

        self.bot.task_paginate(ctx, embeds=embeds, restrict=True)

    @util.with_typing
    @commands.has_permissions(send_messages=True)
    @commands.guild_only()
    @google.command(
        aliases=["i", "is"],
        brief="Searches Google Images",
        description="Returns the top Google Images search result",
        usage="[query]",
    )
    async def images(self, ctx, *, query: str):
        data = {
            "cx": self.bot.file_config.main.api_keys.google_cse,
            "q": query,
            "key": self.bot.file_config.main.api_keys.google,
            "searchType": "image",
        }
        items = await self.get_items(self.GOOGLE_URL, data)

        if not items:
            await util.send_with_mention(
                ctx, f"No image search results found for: *{query}*"
            )
            return

        embeds = []
        for item in items:
            link = item.get("link")
            if not link:
                await util.send_with_mention(
                    ctx,
                    "I had an issue processing Google's response... try again later!",
                )
                return
            embeds.append(link)

        self.bot.task_paginate(ctx, embeds=embeds, restrict=True)

    @util.with_typing
    @commands.has_permissions(send_messages=True)
    @commands.guild_only()
    @commands.command(
        aliases=["yt"],
        brief="Searches YouTube",
        description=("Returns the top YouTube search result"),
        usage="[query]",
    )
    async def youtube(self, ctx, *, query: str):
        items = await self.get_items(
            self.YOUTUBE_URL,
            data={
                "q": query,
                "key": self.bot.file_config.main.api_keys.google,
                "type": "video",
            },
        )

        if not items:
            await util.send_with_mention(ctx, f"No video results found for: *{query}*")
            return

        video_id = items[0].get("id", {}).get("videoId")
        link = f"http://youtu.be/{video_id}"

        links = []
        for item in items:
            video_id = item.get("id", {}).get("videoId")
            link = f"http://youtu.be/{video_id}" if video_id else None
            if link:
                links.append(link)

        self.bot.task_paginate(ctx, links, restrict=True)