from api import BotAPI

from discord import Embed


class SafeEmbed(Embed):
    """Wraps embed creation to avoid 400 errors when sending."""

    def add_field(self, *, name, value, inline=True):
        """Wraps the default add_field method with argument length checks.

        parameters:
            name (str): the name of the field
            value (str): the value of the field
            inline (bool): True if the field should be inlined with the last field
        """

        # if the value cannot be stringified, it is not valid
        try:
            value = str(value)
        except Exception:
            value = ""

        if len(name) > 256:
            name = name[:256]
        if len(value) > 256:
            value = value[:256]

        return super().add_field(name=name, value=value, inline=inline)

class EmbedAPI(BotAPI):

    ALLOWED_ACTIONS = set([
        "add_field",
        "clear_fields",
        "insert_field_at",
        "remove_author",
        "remove_field",
        "set_author",
        "set_field_at",
        "set_footer",
        "set_image",
        "set_thumbnail"
    ])

    def new_embed(self, *args, **kwargs):
        return SafeEmbed(*args, **kwargs)

    async def get_embeds_from_message(self, message_id):
        message = await self.bot.fetch_message(message_id)
        if not message:
            return None

        return message.embeds or None

    async def get_embed_from_message(self, message_id):
        embeds = await self.get_embeds_from_message(message_id)
        return embeds[0] if embeds else None

    async def update_embed(self, message_id, embed):
        message = await self.bot.fetch_message(message_id)
        if not message:
            return None

        if message.author.bot:
            return None

        await message.edit(embed=embed)
