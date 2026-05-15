import discord
import asyncio
import io
import chat_exporter
from datetime import datetime
from dashboard import add_ticket


# =========================
# 🎫 PAINEL DE TICKETS
# =========================
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎫 Suporte", style=discord.ButtonStyle.primary)
    async def suporte(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, "suporte")

    @discord.ui.button(label="💰 Compra", style=discord.ButtonStyle.success)
    async def compra(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, "compra")

    @discord.ui.button(label="🐞 Bug", style=discord.ButtonStyle.danger)
    async def bug(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, "bug")

    async def create_ticket(self, interaction: discord.Interaction, tipo: str):

        guild = interaction.guild
        user = interaction.user

        # anti spam
        existing = discord.utils.get(guild.text_channels, name=f"ticket-{user.id}")

        if existing:
            await interaction.response.send_message("❌ Você já tem um ticket aberto!", ephemeral=True)
            return

        category = discord.utils.get(guild.categories, name="🎫 TICKETS")
        if category is None:
            category = await guild.create_category("🎫 TICKETS")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True),
        }

        channel = await guild.create_text_channel(
            name=f"{tipo}-{user.id}",
            category=category,
            overwrites=overwrites
        )

        embed = discord.Embed(
            title=f"🎫 Ticket {tipo}",
            description=f"{user.mention}, explique seu problema.",
            color=0x5865F2
        )

        await channel.send(embed=embed, view=CloseTicketView())

        await interaction.response.send_message(
            f"✅ Ticket criado: {channel.mention}",
            ephemeral=True
        )


# =========================
# 🔒 FECHAR TICKET
# =========================
class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Fechar Ticket", style=discord.ButtonStyle.red)
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        channel = interaction.channel
        user = interaction.user

        await interaction.response.send_message("🔒 Fechando ticket...")

        transcript = await chat_exporter.export(channel)

        file = discord.File(
            io.BytesIO(transcript.encode()),
            filename=f"{channel.name}.html"
        )

        log_channel = interaction.guild.get_channel(1504666422331183285)

        if log_channel:
            embed = discord.Embed(
                title="📊 Ticket fechado",
                description=f"Fechado por {user.mention}",
                color=0xff0000,
                timestamp=datetime.utcnow()
            )

            await log_channel.send(embed=embed, file=file)

        add_ticket(
            title=channel.name,
            user=str(user),
            data=str(datetime.utcnow())
        )

        await asyncio.sleep(3)
        await channel.delete()