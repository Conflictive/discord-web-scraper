import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import scraper

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")


@bot.command()
async def sales(ctx):
    skins = scraper.get_skin_sales()

    if not skins:
        await ctx.send("There was an issue getting the skins on sale.")
        return

    message = "**This Week's Skin Sales:**\n" + "\n".join(skins)

    await ctx.send(message)


bot.run(TOKEN)
