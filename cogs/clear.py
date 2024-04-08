import disnake
from disnake.ext import commands


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def clear(self, interaction, amount: int):
        await interaction.response.send_message(f"Удалено {amount} сообщений")
        await interaction.channel.purge(limit=amount + 1)

def setup(bot):
    bot.add_cog(Clear(bot))
