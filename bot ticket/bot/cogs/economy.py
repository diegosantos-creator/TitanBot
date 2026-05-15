import discord
from discord.ext import commands
import json
import os
import random
from datetime import datetime, timedelta


DATA_FILE = "economy.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# =========================
# 💰 ECONOMY SYSTEM
# =========================
class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.data = load_data()

    # =========================
    # 💰 BALANCE
    # =========================
    @commands.hybrid_command(name="balance")
    async def balance(self, ctx):

        user = str(ctx.author.id)

        if user not in self.data:
            self.data[user] = {"coins": 0, "last_daily": None}

        save_data(self.data)

        embed = discord.Embed(
            title="💰 Carteira",
            description=f"Coins: {self.data[user]['coins']}",
            color=0x00ff99
        )

        await ctx.send(embed=embed)

    # =========================
    # 🎁 DAILY (ESTILO PROFISSIONAL)
    # =========================
    @commands.hybrid_command(name="daily")
    async def daily(self, ctx):

        user = str(ctx.author.id)

        if user not in self.data:
            self.data[user] = {"coins": 0, "last_daily": None}

        now = datetime.utcnow()

        last = self.data[user]["last_daily"]

        if last:
            last_time = datetime.fromisoformat(last)
            if now - last_time < timedelta(hours=24):
                return await ctx.send("⏳ Você já pegou seu daily hoje. Volte amanhã!")

        # 💰 recompensa variável (estilo bot grande)
        reward = random.randint(100, 500)

        self.data[user]["coins"] += reward
        self.data[user]["last_daily"] = now.isoformat()

        save_data(self.data)

        embed = discord.Embed(
            title="🎁 Daily coletado!",
            description=f"Você ganhou **{reward} coins**!",
            color=0xffcc00
        )

        await ctx.send(embed=embed)

    # =========================
    # 🛒 LOJA
    # =========================
    @commands.hybrid_command(name="shop")
    async def shop(self, ctx):

        embed = discord.Embed(
            title="🛒 Loja do Servidor",
            description=(
                "🎮 VIP - 1000 coins\n"
                "💎 Cargo Especial - 2000 coins\n"
                "🎫 Ticket Prioritário - 500 coins"
            ),
            color=0x5865F2
        )

        await ctx.send(embed=embed)

    # =========================
    # 🛍 BUY ITEM
    # =========================
    @commands.hybrid_command(name="buy")
    async def buy(self, ctx, item: str):

        user = str(ctx.author.id)

        if user not in self.data:
            self.data[user] = {"coins": 0, "last_daily": None}

        item = item.lower()

        shop_items = {
            "vip": 1000,
            "cargo": 2000,
            "ticket": 500
        }

        if item not in shop_items:
            return await ctx.send("❌ Item não encontrado na loja.")

        price = shop_items[item]

        if self.data[user]["coins"] < price:
            return await ctx.send("❌ Você não tem coins suficientes.")

        self.data[user]["coins"] -= price
        save_data(self.data)

        await ctx.send(f"✅ Você comprou **{item}** por {price} coins!")


async def setup(bot):
    await bot.add_cog(Economy(bot))