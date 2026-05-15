import discord
from discord.ext import commands
from datetime import datetime, timedelta
import json
import os


WARN_FILE = "warns.json"


# =========================
# 🧠 STORAGE WARNS
# =========================
def load_warns():
    if not os.path.exists(WARN_FILE):
        return {}
    with open(WARN_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_warns(data):
    with open(WARN_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# =========================
# 🛡 MODERAÇÃO V3
# =========================
class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.warns = load_warns()
        self.message_cache = {}

    # =========================
    # 📊 LOGS
    # =========================
    async def log(self, guild, embed):
        log_channel = discord.utils.get(guild.text_channels, name="mod-logs")

        if log_channel:
            await log_channel.send(embed=embed)

    # =========================
    # ⚠️ WARN SYSTEM
    # =========================
    @commands.hybrid_command(name="warn")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason="Sem motivo"):

        user_id = str(member.id)

        if user_id not in self.warns:
            self.warns[user_id] = []

        self.warns[user_id].append({
            "reason": reason,
            "moderator": str(ctx.author),
            "date": str(datetime.utcnow())
        })

        save_warns(self.warns)

        count = len(self.warns[user_id])

        embed = discord.Embed(
            title="⚠️ Warn aplicado",
            description=f"{member.mention} recebeu warn\nMotivo: {reason}\nTotal: {count}",
            color=0xffcc00,
            timestamp=datetime.utcnow()
        )

        await ctx.send(embed=embed)
        await self.log(ctx.guild, embed)

        # 🚨 AUTO BAN
        if count >= 3:
            await member.ban(reason="3 warns acumulados")

            embed = discord.Embed(
                title="🔨 Auto-ban",
                description=f"{member.mention} foi banido por 3 warns",
                color=0xff0000
            )

            await ctx.send(embed=embed)
            await self.log(ctx.guild, embed)

            self.warns[user_id] = []
            save_warns(self.warns)

    # =========================
    # 🔇 TIMEOUT (MUTE)
    # =========================
    @commands.hybrid_command(name="mute")
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, minutes: int, *, reason="Sem motivo"):

        duration = timedelta(minutes=minutes)

        await member.timeout(duration, reason=reason)

        embed = discord.Embed(
            title="🔇 Mute aplicado",
            description=f"{member.mention} mutado por {minutes} min\nMotivo: {reason}",
            color=0x5865F2,
            timestamp=datetime.utcnow()
        )

        await ctx.send(embed=embed)
        await self.log(ctx.guild, embed)

    # =========================
    # 🚪 KICK
    # =========================
    @commands.hybrid_command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Sem motivo"):

        await member.kick(reason=reason)

        embed = discord.Embed(
            title="🚪 Kick",
            description=f"{member.mention} foi kickado\nMotivo: {reason}",
            color=0xff9900,
            timestamp=datetime.utcnow()
        )

        await ctx.send(embed=embed)
        await self.log(ctx.guild, embed)

    # =========================
    # 🔨 BAN
    # =========================
    @commands.hybrid_command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Sem motivo"):

        await member.ban(reason=reason)

        embed = discord.Embed(
            title="🔨 Ban",
            description=f"{member.mention} foi banido\nMotivo: {reason}",
            color=0xff0000,
            timestamp=datetime.utcnow()
        )

        await ctx.send(embed=embed)
        await self.log(ctx.guild, embed)

    # =========================
    # 🧹 CLEAR
    # =========================
    @commands.hybrid_command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):

        await ctx.channel.purge(limit=amount)

        msg = await ctx.send(f"🧹 {amount} mensagens apagadas")
        await msg.delete(delay=3)

    # =========================
    # 🚨 ANTI-SPAM
    # =========================
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if message.author.bot:
            return

        user_id = message.author.id

        # cache de mensagens
        if user_id not in self.message_cache:
            self.message_cache[user_id] = []

        self.message_cache[user_id].append(datetime.utcnow())

        # remove mensagens antigas (janela de 5s)
        self.message_cache[user_id] = [
            t for t in self.message_cache[user_id]
            if (datetime.utcnow() - t).seconds < 5
        ]

        # 🚨 flood detectado
        if len(self.message_cache[user_id]) >= 5:

            try:
                await message.author.timeout(
                    timedelta(minutes=5),
                    reason="Anti-spam automático"
                )

                embed = discord.Embed(
                    title="🚨 Anti-spam ativado",
                    description=f"{message.author.mention} foi mutado por spam",
                    color=0xff0000
                )

                await message.channel.send(embed=embed)
                await self.log(message.guild, embed)

            except:
                pass

            self.message_cache[user_id] = []


async def setup(bot):
    await bot.add_cog(Moderation(bot))