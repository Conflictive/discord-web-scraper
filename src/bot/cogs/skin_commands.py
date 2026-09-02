"""cogs.skin_commands
~~~~~~~~~~~~~~~~~~
This module contains the 'SkinCommands' Cog, providing commands for any skin related functions.
It handles skin validation from user input and fetching and displaying current skin sales.

Key Commands:
    - !sales: Fetches and returns the list of current skin sales.
    - !skin_exist: Validates if a skin name is legitimate.
"""

import httpx
from discord.ext import commands

import src.database.repositories.skin_repo as skin

API_BASE_URL = "http://localhost:8000"


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
    async def skins(self, ctx: commands.Context, *, message: str) -> None:
        """Returns a list containing all of a champion's skins.

        Queries the external FastAPI backend for skins belonging to the
        specified champion.

        Args:
            ctx: The Discord context object for the command invocation.
            message: The champion name to search for (e.g., "Rammus", "Miss Fortune").
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{API_BASE_URL}/champions/{message}/skins",
                    timeout=5.0,
                )

                if response.status_code == 404:
                    reply = f"Could not find champion '{message}'."
                elif response.status_code == 200:
                    data = response.json()
                    name, skins = data

                    if not skins:
                        reply = f"No skins found for **{name}**."
                    else:
                        reply = f"**{name}:**\n" + "\n".join(skins)
                else:
                    reply = "An unexpected error occurred. Please try again later."

            except httpx.RequestError as exc:
                # Triggers if the FastAPI backend server is offline or unreachable
                reply = "Unable to connect to the skin database service."
                print(f"HTTP Request failed: {exc}")

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
