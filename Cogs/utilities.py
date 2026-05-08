from discord.ext import commands
from skins_manager import validator, scraper


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"We have logged in as {self.bot.user}")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def sales(self, ctx):
        """Gets current skin sales from the web scraper and formats and returns them to the user"""
        skins = scraper.get_skin_sales()

        if not skins:
            await ctx.send("There was an issue getting the skins on sale.")
            return

        message = "**This Week's Skin Sales:**\n" + "\n".join(skins)

        await ctx.send(message)

    @commands.command()
    async def skin_exist(self, ctx, *, message):
        """Check if the users input is a valid skin"""
        await ctx.send(validator.check_skin(message))


async def setup(bot):
    await bot.add_cog(Utilities(bot))
