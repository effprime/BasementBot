from cogs import BasicPlugin
from discord.ext import commands
from utils.embed import SafeEmbed
from utils.helpers import *


def setup(bot):
    bot.add_cog(Embedder(bot))


class Embedder(BasicPlugin):

    PLUGIN_NAME = "Embedder"
    HAS_CONFIG = False

    EXAMPLE_JSON = """
    {
        "embeds": [
            {
                {
                    "author": {
                        "name": "Embed Name"
                    },
                    "fields": [
                        {
                            "name": "Field name",
                            "value": "Field value"
                        },
                        {
                            "name": "Field name",
                            "value": "Field value"
                        },
                        {
                            "name": "Field name",
                            "value": "Field value"
                        },
                    ]
                }
            },
            {
                {
                    "author": {
                        "name": "Embed Name"
                    },
                    "fields": [
                        {
                            "name": "Field name",
                            "value": "Field value"
                        },
                        {
                            "name": "Field name",
                            "value": "Field value"
                        },
                        {
                            "name": "Field name",
                            "value": "Field value"
                        },
                    ]
                }
            }
        ]
    }"""

    async def preconfig(self):
        self.helped = set()

    @commands.has_permissions(send_messages=True)
    @commands.command(
        brief="Generates embeds from uploaded JSON",
        description="Looks for an 'embeds' array in the JSON and renders each embed",
        usage="help",
    )
    async def upload_embeds(self, ctx, *args):
        if len(args) != 0 and args[0] == "help":
            await tagged_response(
                ctx, f"Upload a JSON like this: ```{self.EXAMPLE_JSON}```"
            )
            return

        if not ctx.message.attachments:
            await priv_response(ctx, "Please provide a JSON file for your embed(s)")
            return

        request_body = await get_json_from_attachment(ctx, ctx.message)
        if not request_body:
            return

        embeds = await self.get_embeds_from_request(request_body)
        if not embeds:
            await priv_response(
                ctx, "I was unable to generate any embeds from your request"
            )
            return

        sent_messages = []
        delete = False
        for embed in embeds:
            try:
                # in theory this could spam the API?
                sent_message = await ctx.send(embed=embed)
                sent_messages.append(sent_message)
            except Exception:
                delete = True

        if delete:
            if args and args[0] == "keep":
                await priv_response(ctx, "I couldn't generate all of your embeds")
                return

            for message in sent_messages:
                await message.delete()

            await priv_response(
                ctx,
                "I couldn't generate all of your embeds, so I gave you a blank slate. Use `keep` if you want to keep them next time",
            )

    @staticmethod
    def get_embeds_from_request(request):
        embeds = []
        try:
            for embed_request in request.get("embeds", []):
                embeds.append(SafeEmbed.from_dict(embed_request))
        except Exception:
            pass

        return embeds

    def generate_creation_helper_embed(self):
        description = f"`{self.bot.config.main.required.command_prefix}create_embed` and use the commands below"

        embed = SafeEmbed(title="Embed generation guide", description=description)

        embed.add_field(name="`.add_field <name> <value> <inline (True by default)>`", value="Adds a name-value field", inline=False)
        embed.add_field(name="`.clear_fields`", value="Clears all fields", inline=False)
        embed.add_field(name="`.insert_field_at <index>`", value="Inserts a field at a given index", inline=False)
        embed.add_field(name="`.remove_author`", value="Removes the author", inline=False)
        embed.add_field(name="`.remove_field <index>`", value="Removes a field at a given index", inline=False)
        embed.add_field(name="`.set_author`", value="Sets the author", inline=False)
        embed.add_field(name="`.set_field_at <index>`", value="Updates a field at a given index", inline=False)
        embed.add_field(name="`.set_footer <value>`", value="Sets the footer", inline=False)
        embed.add_field(name="`.set_image <url>`", value="Sets the image", inline=False)
        embed.add_field(name="`.set_thumbnail <url>`", value="Sets the thumbnail", inline=False)

        return embed

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




    @commands.has_permissions(send_messages=True)
    @commands.command(
        brief="Creates an embed",
        description="Looks for a 'embeds' array in the JSON and renders each embed",
        usage="help"
    )
    async def create_embed(self, ctx, args):
        # generate raw embed
        template_embed = SafeEmbed()
        message = await tagged_response(ctx, content="Here is your raw template", embed=embed)



    
