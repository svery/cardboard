import logging

import discord
from discord.ext import commands
from discord import app_commands

from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.management.base import BaseCommand
from django.test import Client

from puzzles.models import Puzzle
logger = logging.getLogger(__name__)


c = Client()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)
hunt=settings.BOT_ACTIVE_HUNT

@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print("Synced the commands.")
        await sync_to_async(c.login)(username="discord_bot", password="thisisnotarealpassword")
        print("Logged in as discord_bot")

    except Exception as e:
        print(f"Sync command failed with error: {e}")

@bot.tree.command(name="pingpuzzbot", description="Sends the bot's latency.") # this decorator makes a slash command
async def pingpuzzbot(interaction: discord.Interaction): # a slash command will be created with the name "ping"
    await interaction.response.send_message(f"Pong! Latency is {bot.latency}")


@bot.tree.command(name="solve", description="Mark the puzzle as solved.")
@app_commands.describe(answer="Answer to the puzzle")
async def solve(interaction: discord.Interaction, answer: str):
    try:
        channel_id = interaction.channel.id
        matching_puzzles = await sync_to_async(list)(Puzzle.objects.filter(chat_room__text_channel_id=channel_id))
        if not matching_puzzles:
            allpuzzles = await sync_to_async(list)(Puzzle.objects.all())
            all_channel_ids = [sync_to_async(sync_to_async(puz.__getattribute__)("chat_room").__getattribute__)("text_channel_id")() for puz in allpuzzles]
            await interaction.response.send_message(f"Puzzle {channel_id} not found. Hunt: {hunt}, Puzzles: {allpuzzles}, Channel IDs: {all_channel_ids}  (Please use this command in the puzzle-specific channel.)", ephemeral=True)
            return
        puzzle = matching_puzzles[0]
        if puzzle.status == "SOLVED":
            await interaction.response.send_message("This puzzle has already been solved.", ephemeral=True)
            return
        else:
            await sync_to_async(c.post)(f"/api/v1/puzzles/{puzzle.id}/answers", {"text": answer})
            await interaction.response.send_message(f"Solved as `{answer}`!")
    except Exception as e:
        logger.exception(f"announce_puzzle_unlock failed with error: {e}")
        if not interaction.response.is_done():
            await interaction.response.send_message(
                f"An unexpected error occurred: {e}",
                ephemeral=True
            )
        else:
            await interaction.followup.send(
                f"An unexpected error occurred: {e}",
                ephemeral=True
            )

# Run the bot with your token
def main():
    bot.run(settings.DISCORD_API_TOKEN)


class Command(BaseCommand):
    help = "Run the Discord bot."

    def handle(self, *args, **options):
        main()
