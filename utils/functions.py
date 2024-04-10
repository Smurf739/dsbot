import disnake

import datetime
import pytz


def get_time_now():
    return datetime.datetime.now().astimezone(pytz.timezone("Europe/Moscow")).strftime("%H:%M")