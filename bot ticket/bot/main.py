import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

# =========================
# 🔐 ENV
# =========================
load_dotenv()

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN não encontrado no .env")


# =========================
# 🤖 INTENTS
# =========================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True


# =========================
# 🤖 BOT
# =========================
bot = commands.Bot(command_prefix="!", intents=intents)


# =========================
# 📦 LOAD COGS
# =========================
async def load_cogs():
    cogs_path = Path("./cogs")

    for file in cogs_path.glob("*.py"):
        if file.name.startswith("_"):
            continue

        extension = f"cogs.{file.stem}"

        try:
            await bot.load_extension(extension)
            print(f"[COG] {file.stem} carregada")
        except Exception as e:
            print(f"[ERRO] {file.stem}: {e}")


# =========================
# 🚀 READY EVENT
# =========================
@bot.event
async def on_ready():
    print("=" * 50)
    print(f"{bot.user} está online!")
    print("=" * 50)

    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} slash commands sincronizados")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")

    await bot.change_presence(
        activity=discord.Game(name="Tickets + Moderação + Economia"),
        status=discord.Status.online
    )


# =========================
# 🚀 START BOT
# =========================
async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())