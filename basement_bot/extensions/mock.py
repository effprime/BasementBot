import base
import discord
import util
from discord.ext import commands


async def setup(bot):
    await bot.add_cog(Mocker(bot=bot))


class MockEmbed(discord.Embed):
    def __init__(self, *args, **kwargs):
        message = kwargs.pop("message")
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        mock_string = self.mock_string(message)
        self.title = f'"{mock_string}"'
        self.description = user.name
        self.set_thumbnail(url=user.avatar_url)
        self.color = discord.Color.greyple()

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


class Mocker(base.BaseCog):

    SEARCH_LIMIT = 20

    @util.with_typing
    @commands.guild_only()
    @commands.command(
        aliases=["sb"],
        brief="Mocks a user",
        description=("Mocks the most recent message by a user"),
        usage="@user",
    )
    async def mock(self, ctx, user_to_mock: discord.Member):
        if not user_to_mock:
            await ctx.send_deny_embed("You must tag a user if you want to mock them!")
            return

        if user_to_mock.bot:
            user_to_mock = ctx.author

        prefix = await self.bot.get_prefix(ctx.message)

        mock_message = None
        async for message in ctx.channel.history(limit=self.SEARCH_LIMIT):
            if message.author == user_to_mock and not message.content.startswith(
                prefix
            ):
                mock_message = message.clean_content
                break

        if not mock_message:
            await ctx.send_deny_embed(f"No message found for user {user_to_mock}")
            return

        embed = MockEmbed(message=mock_message, user=user_to_mock)
        await ctx.send(embed=embed)
