from disnake.ext import commands
import disnake
from config import category_voice_create, voice_create_channel, \
    voice_settings_channel

async def text_func(category=None, settings_room=None):
    if settings_room is None:
        settings_room = await category.create_text_channel(
            name="Настройка "
                 "комнаты")
    else:
        a = [message async for message in settings_room.history()]
        await settings_room.purge(limit=len(a))
    embed = disnake.Embed(
        title="📦 Настройка комнаты",
        description="Выбери подходящие кнопки, чтобы настроить свою руму",
        color=0x313338)

    embed.add_field(name="",
                    value="📏 — установить лимит\n"
                          "🔐 — закрыть/открыть комнату\n"
                          "🛡️ — забрать/выдать доступ к руме\n"
                          "👑 — передать владельца\n"
                          "🔊 — забрать/выдать право говорить")
    embed.add_field(name="",
                    value="✏️ — сменить название\n"
                          "👊🏼 — выгнать из комнаты\n"
                          "🕵🏻 — скрыть/открыть комнату\n"
                          "🧹 — сбросить права пользователя\n"
                          "ℹ️ — информация о комнате")
    embed.set_footer(
        text="Использовать можно только в голосовом канале")

    await settings_room.send(embed=embed)

async def create(this_guild):
    global voice_settings_channel
    global voice_create_channel
    global category_voice_create

    category = await this_guild.create_category(
        name="Приватные комнаты")
    category_voice_create = category.id

    settings_room = await category.create_text_channel(
        name="Настройка "
             "комнаты")



    voice_room = await category.create_voice_channel(
        name="Создать комнату")
    voice_settings_channel = settings_room.id
    voice_create_channel = voice_room.id

    embed = disnake.Embed(
        title="📦 Настройка комнаты",
        description="Выбери подходящие кнопки, чтобы настроить свою руму",
        color=0x313338)

    embed.add_field(name="",
                    value="📏 — установить лимит\n"
                          "🔐 — закрыть/открыть комнату\n"
                          "🛡️ — забрать/выдать доступ к руме\n"
                          "👑 — передать владельца\n"
                          "🔊 — забрать/выдать право говорить")
    embed.add_field(name="",
                    value="✏️ — сменить название\n"
                          "👊🏼 — выгнать из комнаты\n"
                          "🕵🏻 — скрыть/открыть комнату\n"
                          "🧹 — сбросить права пользователя\n"
                          "ℹ️ — информация о комнате")
    embed.set_footer(
        text="Использовать можно только в голосовом канале")

    await settings_room.send(embed=embed)


class load():
    def __init__(self, bot):
        self.bot = bot

    async def create_channels(self, this_guild):
        is_voice = False
        is_text = False
        is_category = False
        global category_voice_create
        global voice_settings_channel
        global voice_create_channel
        category = None
        for i in this_guild.categories:
            if i.name == "Приватные комнаты" or i.name == "Private rooms":
                category = i
                print(i, category)
                is_category = True
                category_voice_create = i.id
                for j in i.channels:
                    if j.name.lower() == "настройка-комнаты":
                        voice_settings_channel = j.id
                        is_text = True
                        await text_func(i, j)


                    elif j.name.lower() == "создать комнату":
                        voice_create_channel = j.id
                        is_voice = True

                break

        if is_text is False and is_voice is False and is_category is False:
            await create(this_guild)
        elif is_voice is False:
            voice_room = await category.create_voice_channel(
                name="Создать комнату")
            voice_create_channel = voice_room.id
        elif is_text is False:
            await text_func(category)

        print(category_voice_create, voice_create_channel, voice_settings_channel)

