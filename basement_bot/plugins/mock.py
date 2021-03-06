import cogs
import decorate
from discord.ext import commands


def setup(bot):
    bot.add_cog(Mocker(bot))


class Mocker(cogs.BasicPlugin):

    PLUGIN_NAME = __name__
    HAS_CONFIG = False
    SEARCH_LIMIT = 20

    @staticmethod
    def mock_string(string):
        mock = ""
        i = True
        for char in string:
            if i:
                mock += char.upper()
            else:
                mock += char.lower()
            if char != " ":
                i = not i
        return mock

    @decorate.with_typing
    @commands.has_permissions(send_messages=True)
    @commands.command(
        aliases=["sb"],
        brief="Mocks a user",
        description=("Mocks the most recent message by a user"),
        usage="@user",
    )
    async def mock(self, ctx):
        user_to_mock = ctx.message.mentions[0] if ctx.message.mentions else None

        if not user_to_mock:
            await self.bot.h.tagged_response(
                ctx, "You must tag a user if you want to mock them!"
            )
            return

        if user_to_mock.bot:
            user_to_mock = ctx.author

        mock_message = None
        async for message in ctx.channel.history(limit=self.SEARCH_LIMIT):
            if message.author == user_to_mock and not message.content.startswith(
                self.bot.config.main.required.command_prefix
            ):
                mock_message = message.content
                break

        if not mock_message:
            await self.bot.h.tagged_response(
                ctx, f"No message found for user {user_to_mock}"
            )
            return

        filtered_message = self.bot.h.sub_mentions_for_usernames(mock_message)
        mock_string = self.mock_string(filtered_message)
        embed = self.bot.embed_api.Embed(
            title=f'"{mock_string}"', description=user_to_mock.name
        )
        embed.set_thumbnail(url=user_to_mock.avatar_url)

        await self.bot.h.tagged_response(ctx, embed=embed)
