import base
import util
from discord.ext import commands


def setup(bot):
    bot.add_cog(Translator(bot=bot))


class Translator(base.BaseCog):

    HAS_CONFIG = False

    API_URL = "https://api.mymemory.translated.net/get?q={}&langpair={}|{}"

    @util.with_typing
    @commands.has_permissions(send_messages=True)
    @commands.command(
        brief="Translates a message",
        description="Translates a given input message to another language",
        usage='"[message (in quotes)]" [src language code (en)] [dest language code (es)]',
    )
    async def translate(self, ctx, message, src: str, dest: str):
        response = await util.http_call(
            "get",
            self.API_URL.format(message, src, dest),
        )
        translated = response.get("responseData", {}).get("translatedText")

        if not translated:
            await util.send_with_mention(ctx, "I could not translate your message")
            return

        await util.send_with_mention(ctx, translated)