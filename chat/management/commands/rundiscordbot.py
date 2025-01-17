import discord
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from discord.ext import commands
import cardboard.settings
from accounts.models import Puzzler
from django.test import Client

from puzzles.models import Puzzle
from puzzles.puzzle_tag import PuzzleTag


c = Client()

print(discord.__version__)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)
hunt=settings.BOT_ACTIVE_HUNT

@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print("Synced the commands.")
    except Exception as e:
        print(f"Sync command failed with error: {e}")

@bot.command(name="pingpuzzbot", description="Sends the bot's latency.") # this decorator makes a slash command
async def pingpuzzbot(ctx): # a slash command will be created with the name "ping"
    await ctx.respond(f"Pong! Latency is {bot.latency}")


@bot.command(name="solve", description="Mark the puzzle as solved.")
@app_commands.describe(answer="Answer to the puzzle")
async def solve(ctx: interactions.SlashContext, answer: str):
    channel_id = ctx.channel.id
    try:
        match = list(Puzzle.objects.filter(hunt==settings.BOT_ACTIVE_HUNT, chat_room.text_channel_id==channel_id))
        if not match:
            await ctx.channel.send("Puzzle not found. (Please use this command in the puzzle-specific channel.)")
        elif match[0].status == "SOLVED":
            await ctx.channel.send("This puzzle has already been solved.")
        else:
            puzzle_id = match[0].id
            temp_user = Puzzler.objects.create_user(username="test", email="test@ing.com", password="testingpwd")
            c.login(username="test", password="testingpwd")
            assign_perm("hunt_access", self.temp_user, self.hunt)
            c.post(f"/api/v1/puzzles/{puzzle_id}/answers", {"text": answer})
            await ctx.channel.send(f"Solved as `{answer}`!")
    except Exception as e:
        logger.exception(f"announce_puzzle_unlock failed with error: {e}")

# Run the bot with your token
bot.run(settings.DISCORD_API_TOKEN)
