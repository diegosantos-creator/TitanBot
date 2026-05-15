import discord
from discord.ext import commands
from datetime import datetime


class Automations(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 💬 RESPOSTAS AUTOMÁTICAS
    # =========================
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if message.author.bot:
            return

        content = message.content.lower()

        # 👋 boas-vindas simples por mensagem (fallback)
        if "oi" in content or "ola" in content:
            await message.channel.send(f"👋 Olá {message.author.mention}, tudo bem?")

        # 💰 info economia
        if "dinheiro" in content:
            await message.channel.send("💰 Use !balance para ver seu saldo.")

        # 🎫 tickets
        if "ticket" in content:
            await message.channel.send("🎫 Use o painel de tickets para abrir um chamado.")

        await self.bot.process_commands(message)


async def setup(bot):
    await bot.add_cog(Automations(bot))