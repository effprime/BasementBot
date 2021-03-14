import cogs
from discord.ext import commands


def setup(bot):
    return bot.process_plugin_setup(cogs=[IPInfo])


class IPInfo(cogs.BaseCog):

    API_URL = "https://ipinfo.io"
    IP_ICON_URL = "https://cdn.icon-icons.com/icons2/1858/PNG/512/iconfinder-dedicatedipaddress-4263513_117864.png"

    @commands.command(
        name="ipinfo",
        alias=["ip"],
        brief="Gets IP info",
        description="Gets IP info (geodata) from a given IP",
    )
    async def get_info(self, ctx, ip_address: str):
        response = await self.bot.http_call("get", f"{self.API_URL}/{ip_address}/json")

        if not response.get("ip"):
            await self.tagged_response(ctx, "I couldn't find that IP")
            return

        response.pop("readme", None)
        response.pop("status_code", None)

        embed = self.bot.embed_api.Embed.from_kwargs(
            title=f"IP info for {ip_address}", all_inline=True, **response
        )

        embed.set_thumbnail(url=self.IP_ICON_URL)

        await self.tagged_response(ctx, embed=embed)