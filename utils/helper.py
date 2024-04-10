import disnake

from database import VoiceDb
from utils.functions import get_time_now



def is_leader(func):
    pass
    async def inner(*args, **kwargs):
        a = VoiceDb()
        inter = args[2]
        user = await a.get_user(inter.user.voice.channel.id)
        if inter.user.id == user[0]:
            await func(*args, **kwargs)
        else:
            await inter.response.send_message(embed=disnake.Embed(title="Ошибка",
                description=f"❗ | {inter.user.mention}, ты не лидер этой комнаты!",
                color=0x313338
            ).set_footer(text=f"Сегодня, в{get_time_now()}"), ephemeral=True)

    return inner


def in_voice(func):
    async def inner(*args, **kwargs):
        inter = args[2]
        if inter.user.voice:
            await func(*args, **kwargs)
        else:
            await inter.response.send_message(
                embed=disnake.Embed(title="Ошибка",
                                    description=f"❗ | {inter.user.mention}, ты не находишься в приватной комнате!",
                                    color=0x313338
                                    ).set_footer(
                    text=f"Сегодня, в{get_time_now()}"), ephemeral=True)

    return inner
