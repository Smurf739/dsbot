import datetime

import disnake
from disnake.ext import commands
from database import VoiceDb


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
                date_created = datetime.datetime.now().strftime(
                    "%y years %m month %d days %H hours %M minutes %S seconds")
                print(type(date_created))
                print(date_created)
                await member.move_to(mychannel)
                await VoiceDb().create_room_info(voice_i=mychannel.id,
                                                voice_n=mychannel.name,
                                                date=date_created,
                                                owner=member.id)

        except AttributeError:
            if before.channel == mychannel:
                if len(before.channel.members) == 0:
                    await VoiceDb().remove_room(before.channel.id)
                    await before.channel.delete()
            else:
                pass


def setup(bot):
    bot.add_cog(UserHandler(bot))
