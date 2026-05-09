"""
cogs.skin_commands
~~~~~~~~~~~~~~~~~~
This module contains the 'SkinCommands' Cog, providing commands for any skin related functions.
It handles skin validation from user input and fetching and displaying current skin sales.

Key Commands:
    - !sales: Fetches and returns the list of current skin sales.
    - !skin_exist: Validates if a skin name is legitimate.
"""

from discord.ext import commands
from skins_manager import scraper, validator, storage


class SkinCommands(commands.Cog):
    """
    Commands that are relevant to skins or skin sales
    This cog provides commands for skin validation and fetching the list of current skin sales.

    Attributes:
        bot (commands.Bot): The instance of the running Discord bot.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sales(self, ctx):
        """Gets current skin sales from the web scraper and formats and returns them to the user"""

        # 1. Fetch data from the scraper logic in the skins_manager package
        skins = scraper.get_skin_sales()

        # 2. Handle the cases where the scraper fails (timeouts, 404, etc) gracefully
        if not skins:
            await ctx.send("There was an issue getting the skins on sale.")
            return

        # 3. Format the message into a single string using a join to avoid the need to send multiple messages which might exceed rate limits
        message = "**This Week's Skin Sales:**\n" + "\n".join(skins)

        await ctx.send(message)

    @commands.command()
    async def skin_exist(self, ctx, *, message):
        """Check if the users input is a valid skin"""
        # Uses the validator module to compare the user input to the valid list in the json file
        await ctx.send(validator.check_skin(message))

    @commands.command(usage="!skins <champion> (Example: !skins kha'zix)")
    async def skins(self, ctx, *, message):
        """Returns a list containing all of a champions skins"""
        skins = storage.open_skin_file()
        champion_skins = [skin for skin in skins if skin.endswith(message)]
        champion_name = champion_skins[0]
        champion_skins.pop(0)

        reply = f"**{champion_name}:**\n" + "\n".join(champion_skins)
        await ctx.send(reply)

    @skins.error
    async def skins_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**Missing Champion**\n " + ctx.command.usage)


async def setup(bot):
    """Setup function is used to load the cog when the extension is loaded."""
    await bot.add_cog(SkinCommands(bot))
