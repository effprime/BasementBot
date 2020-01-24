from random import choice
from discord.ext import commands
from utils import tagged_response

def setup(bot):
    bot.add_command(hug)

@commands.command(name="hug")
async def hug(ctx):
    try:
        if not ctx.message.mentions:
            await ctx.send(f"{ctx.author.mention} You hugging the air?")
            return
        
        has_author_mentioned = False
        has_bot_mentioned = False
        for user in ctx.message.mentions:
            if user.id == ctx.author.id:
                has_author_mentioned = True
            elif user.bot:
                has_bot_mentioned = True

        if has_author_mentioned and has_bot_mentioned:
            await ctx.send(f"{ctx.author.mention} You're tyring to hug the bot AND yourself? You got issues")
            return
        elif has_author_mentioned:
            await ctx.send(f"{ctx.author.mention} You tried to hug yourself?")
            return
        elif has_bot_mentioned:
            await ctx.send(f"{ctx.author.mention} You tried to hug the bot?")
            return

        if len(ctx.message.mentions) > 1:
            mentions = [m.mention for m in ctx.message.mentions]
            await ctx.send(choice(hugs).format(user_giving_hug=ctx.author.mention, user_to_hug=", ".join(mentions[:-1]) + ", and " + mentions[-1]))
            return
            
        await ctx.send(choice(hugs).format(user_giving_hug=ctx.author.mention, user_to_hug=ctx.message.mentions[0].mention))
    except:
        await ctx.send(f"I don't know what the fuck you're trying to do!")

hugs = [
    "{user_giving_hug} hugs {user_to_hug} forever and ever and ever",
    "{user_giving_hug} wraps arms around {user_to_hug} and clings forever",
    "{user_giving_hug} hugs {user_to_hug} and gives their hair a sniff",
    "{user_giving_hug} glomps {user_to_hug}",
    "cant stop, wont stop. {user_giving_hug} hugs {user_to_hug} until the sun goes cold",
    "{user_giving_hug} reluctantly hugs {user_to_hug}...",
    "{user_giving_hug} hugs {user_to_hug} into a coma",
    "{user_giving_hug} smothers {user_to_hug} with a loving hug",
    "{user_giving_hug} squeezes {user_to_hug} to death"
]