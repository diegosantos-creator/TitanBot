from __future__ import annotations

import discord
from discord.ext import commands

from config import EMBED_COLOR


class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        guild = member.guild

        channel = discord.utils.get(guild.text_channels, name="boas-vindas")
        if channel is None:
            for text_channel in guild.text_channels:
                perms = text_channel.permissions_for(guild.me)
                if perms.send_messages and perms.embed_links:
                    channel = text_channel
                    break

        if channel is None:
            return

        embed = discord.Embed(
            title="🎉 Bem-vindo(a) ao servidor!",
            description=(
                f"Olá {member.mention}, seja muito bem-vindo(a) ao **{guild.name}**!\n"
                "Esperamos que você tenha uma ótima experiência por aqui."
            ),
            color=EMBED_COLOR,
        )
        embed.add_field(name="👤 Usuário", value=f"{member} (`{member.id}`)", inline=False)
        embed.add_field(
            name="👥 Membros no servidor",
            value=f"{guild.member_count}",
            inline=True,
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Entrada registrada em {guild.name}")

        await channel.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Welcome(bot))
