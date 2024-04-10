import disnake
from disnake.ext import commands


mychannel = None

class UserHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self,member, before, after):
        from config import voice_create_channel
        global mychannel
        try:
            if after.channel.id == voice_create_channel:
                mychannel = await after.channel.category.create_voice_channel(
                    name=member.name
                )
                await member.move_to(mychannel)

        except AttributeError:
            if before.channel == mychannel:
                if len(before.channel.members) == 0:
                    await before.channel.delete()
            else:
                pass


def setup(bot):
    bot.add_cog(UserHandler(bot))
