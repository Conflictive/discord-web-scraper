"""
cogs.utilities

This module contains the 'Utilities' Cog, providing general purpose commands and event listeners.
It handles the on_ready listener and basic connectivity checks using bot.latency

Key Commands:
    - !ping: Returns bot latency.
    - on_ready: Executes function on startup.
"""

from discord.ext import commands


class Utilities(commands.Cog):
    """
    General utility commands and event listeners for the bot.

    This cog provides basic commands like ping and lifecycle event handlers
    such as on_ready.

    Attributes:
        bot (commands.Bot): The instance of the running Discord bot.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Prints a confirmation of log in into the terminal once the bot is started"""
        print(f"We have logged in as {self.bot.user}")

    @commands.command()
    async def ping(self, ctx):
        """Returns the latency of the bots response as a message"""
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")


async def setup(bot):
    """Setup function is used to load the cog when the extension is loaded."""
    await bot.add_cog(Utilities(bot))
