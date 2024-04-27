import disnake

import datetime
import pytz


def get_time_now():
    return datetime.datetime.now().astimezone(pytz.timezone("Europe/Moscow")).strftime("%H:%M")

def get_info(channel, res, interaction, isClose_value, invisible_value):
    embed = disnake.Embed(title=f"<:box:1128055986670805115> Информация о комнате")

    embed.add_field(name="", value=f">>> **Приватная комната:** {channel.mention}\n"
                                   f"**Владелец:** {res[3]}\n**Дата создания:** {res[2]}\n"
                                   f"**Участников:** {len(interaction.user.voice.channel.members)}\n"
                                   f"**Приватность канала:** {isClose_value}\n"
                                   f"**Скрытие комнаты:** {invisible_value}")

    return embed