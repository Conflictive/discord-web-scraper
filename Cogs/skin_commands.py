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
from skins_manager import validator, storage
import database.crud as crud
import database.models as models


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
        """
        Fetches and displays the current week's skin sales.

        Retrieves the latest skin sales data from the web scraper and formats
        it into a single Discord message. If the scraper fails or returns no data,
        sends an error message.

        Args:
            ctx: The Discord context object for the command invocation.

        Sends:
            A formatted Discord message with this week's skin sales list,

        """
        message = "**This week's skin sales:**\n"

        skins = await crud.get_active_sales_with_skins()
        for sale in skins:
            message += f"• {sale.skin.name}: ~~{sale.original_price} RP~~ ➔ **{sale.sale_price} RP**\n"
        await ctx.send(message)

    @commands.command()
    async def skin_exist(self, ctx, *, message):
        """
        Validates whether the provided skin name exists in the database.

        Compares the user's input against the complete list of valid skins
        using the validator module.

        Args:
            ctx: The Discord context object for the command invocation.
            message (str): The skin name to validate.

        Raises:
            commands.MissingRequiredArgument: If no skin name is provided.

        Sends:
            A Discord message indicating whether the skin is valid (True) or not (False).
        """
        # Uses the validator module to compare the user input to the valid list in the json file
        await ctx.send(validator.check_skin(message))

    @commands.command(usage="!skins <champion> (Example: !skins kha'zix)")
    async def skins(self, ctx, *, message):
        """Returns a list containing all of a champions skins.

        Filters the skin database for all skins belonging to a specified champion.
        The search is case-insensitive and ignores spaces, so both 'miss fortune'
        and 'missfortune' will match the champion.

        Args:
            ctx: The Discord context object for the command invocation.
            message (str): The champion name to search for (e.g., "Rammus", "Miss Fortune").

        Raises:
            commands.MissingRequiredArgument: If no champion name is provided.

        Sends:
            A formatted Discord message with the champion name and their complete skin list.
        """

        # Temp solution to prevent single letter matching
        # Example: !skins t would return both urgot and sett currently because of how endswith works
        if len(message) < 3:
            return

        skins = await storage.open_skin_file()

        # Remove any trailing whitespace from the message
        # Make the message lowercase for easier comparison
        # Remove spaces so both "miss fortune" and "missfortune" are valid
        clean_message = message.strip().lower().replace(" ", "")

        # Gets all skins that have the matching champion name
        champion_skins = [
            skin
            for skin in skins
            if skin.lower().replace(" ", "").endswith(clean_message)
        ]

        # Save and remove the champion name
        # The first index holds only the champion name e.g "Rammus"
        champion_name = champion_skins[0]
        champion_skins.pop(0)

        reply = f"**{champion_name}:**\n" + "\n".join(champion_skins)
        await ctx.send(reply)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        Global error handler for commands in this cog.

        Handles various command errors gracefully:
        - CommandNotFound: Silently ignores unknown commands.
        - MissingRequiredArgument: Sends usage information to the user.
        - Other errors: Logs unhandled errors to the console.

        Args:
            ctx: The Discord context object for the command invocation.
            error: The exception that was raised during command execution.
        """
        # Check for error type
        if isinstance(error, commands.CommandNotFound):
            return  # Ignore this error

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"**Missing argument** \n {ctx.command.usage}")

        else:
            print(f"Unhandled error: {error}")


async def setup(bot):
    """Setup function used to load the cog when the extension is loaded."""
    await bot.add_cog(SkinCommands(bot))
