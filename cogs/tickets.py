import discord
from discord.ext import commands
from views.ticket_view import TicketView


class Tickets(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ticket", description="Abre o painel de tickets")
    async def ticket(self, ctx):

        embed = discord.Embed(
            title="🎫 Central de Tickets",
            description=(
                "Clique em uma opção abaixo:\n\n"
                "🎫 Suporte\n"
                "💰 Compra\n"
                "🐞 Bug"
            ),
            color=0x5865F2
        )

        await ctx.send(embed=embed, view=TicketView())


async def setup(bot):
    await bot.add_cog(Tickets(bot))