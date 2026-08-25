"""cogs.skin_commands
~~~~~~~~~~~~~~~~~~
This module contains the 'SkinCommands' Cog, providing commands for any skin related functions.
It handles skin validation from user input and fetching and displaying current skin sales.

Key Commands:
    - !sales: Fetches and returns the list of current skin sales.
    - !skin_exist: Validates if a skin name is legitimate.
"""

from discord.ext import commands

import src.database.repositories.skin_repo as skin


class SkinCommands(commands.Cog):
    """Commands that are relevant to skins or skin sales
    This cog provides commands for skin validation and fetching the list of current skin sales.

    Attributes:
        bot (commands.Bot): The instance of the running Discord bot.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sales(self, ctx):
        """Fetches and displays the current week's skin sales.

        Retrieves the latest skin sales data from the web scraper and formats
        it into a single Discord message. If the scraper fails or returns no data,
        sends an error message.

        Args:
            ctx: The Discord context object for the command invocation.

        Sends:
            A formatted Discord message with this week's skin sales list,

        """
        message = "**This week's skin sales:**\n"

        skins = await skin.get_active_sales_with_skins()
        for sale in skins:
            message += f"• {sale.skin.name}: ~~{sale.original_price} RP~~ ➔ **{sale.sale_price} RP**\n"
        await ctx.send(message)

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
        try:
            name, skins = await skin.get_champion_skins(message)

            # TODO: Improve error handling to be more specific and robust
            if len(skins) < 1:
                reply = "Something went wrong."
            else:
                reply = f"**{name}:**\n" + "\n".join(skins)
        except Exception as e:
            reply = "Something went wrong."
            print(e)

        await ctx.send(reply)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Global error handler for commands in this cog.

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
