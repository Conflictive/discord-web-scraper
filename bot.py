"""
Main Entry Point
~~~~~~~~~~~~~~~~
The primary script for the bot.
This file uses dotenv to get environment variables, initialises the bot instance,
configures intents and loads all of the command Cogs from the ./cogs directory.

Environment Variables:
    - TOKEN: The discord bot token provided by the developer portal.

Dependencies:
    - os, dotenv: For loading environment variables
    - discord.ext.commands: For bot framework and Cog management.
"""

import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# 1. Load environment variables from the .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")


class Bot:
    """
    Bot setup that configures intents and loads all of the command Cogs from the ./cogs directory.
    """

    def __init__(self):
        # 2. Configure Intents: Required for reading message content in prefix commands
        intents = discord.Intents.default()
        intents.message_content = True

        self.bot = commands.Bot(command_prefix="!", intents=intents)

    async def load_extensions(self):
        """Iterates through the cogs folder and registers each Python file as an extension."""
        for filename in os.listdir("./cogs"):
            # Avoid using including __init__.py
            if filename.endswith(".py") and filename != "__init__.py":
                # Load using dot-notation: cogs.filename
                # filename[:-3] removes the file extension
                await self.bot.load_extension(f"cogs.{filename[:-3]}")

    async def main(self):
        """Startup for the bot"""
        async with self.bot:
            await self.load_extensions()
            await self.bot.start(TOKEN)


if __name__ == "__main__":
    import asyncio

    try:
        bot = Bot()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        #  Handle the bot being shut down via Ctrl+C
        print("Bot is shutting down...")
