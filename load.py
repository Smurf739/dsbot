from disnake.ext import commands
import disnake
import config
from database import VoiceDb
from utils.helper import is_leader, in_voice
from utils.functions import get_time_now


class VoiceButtons(disnake.ui.View):
    def __init__(self):
        self.voice_db = VoiceDb()
        super().__init__(timeout=None)

    @disnake.ui.button(style=disnake.ButtonStyle.secondary,
                       emoji="📏", custom_id="people")
    @in_voice
    @is_leader
    async def room1_settings(self, message,
                             interaction: disnake.MessageInteraction):
        await interaction.response.send_modal(
            ModalHandler(interaction.user.voice.channel,
                         interaction.user.voice.channel.id, "limit"))



class ModalHandler(disnake.ui.Modal):
    def __init__(self, channel, channel_id, arg):
        self.channel = channel
        self.channel_id = channel_id
        self.voicedb = VoiceDb()
        self.arg = arg
        if self.arg == "limit":
            label = "Укажи лимит."
            custom_id = "limit"
            placeholder = "Укажи количество участников от 0 до 99"
            title = "Изменение названия войса"
        components = [
            disnake.ui.TextInput(label=label, placeholder=placeholder, custom_id=custom_id)
        ]
        super().__init__(title=title, custom_id=custom_id, components=components)

    async def callback(self, interaction: disnake.MessageInteraction) -> None:
        if interaction.text_values is None:
            interaction.response.defer()
        else:
            if self.arg == "limit":
                res = interaction.text_values["limit"]
                if int(res) > 99:
                    res = "99"
                elif int(res) < 0:
                    res = "0"
                await self.channel.edit(user_limit=res)
                await self.voicedb.set_limit(res, self.channel_id)

                await interaction.response.send_message(embed=disnake.Embed(
                    title=f"📦 Комната: {interaction.user.voice.channel.mention}",
                    description="**Ты успешно отредактировал свою комнату!**",
                    color=0x2f3136
                ).add_field(name="", value=f"> {interaction.author.mention}, новый лимит пользователей - **{res}**").set_footer(
                    text=f"Сегодня, в {get_time_now()}").set_thumbnail(interaction.author.avatar),
                    ephemeral=True)



async def text_func(category=None, settings_room=None):
    if settings_room is None:
        settings_room = await category.create_text_channel(
            name="Настройка "
                 "комнаты")
        config.voice_settings_channel = settings_room.id
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

    await settings_room.send(embed=embed, view=VoiceButtons())


async def create(this_guild):
    category = await this_guild.create_category(
        name="Приватные комнаты")
    config.category_voice_create = category.id

    settings_room = await category.create_text_channel(
        name="Настройка "
             "комнаты")

    voice_room = await category.create_voice_channel(
        name="Создать комнату")
    config.voice_settings_channel = settings_room.id
    config.voice_create_channel = voice_room.id

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

    await settings_room.send(embed=embed, view=VoiceButtons())


class load():
    def __init__(self, bot):
        self.bot = bot

    async def create_channels(self, this_guild):
        is_voice = False
        is_text = False
        is_category = False
        category = None
        for i in this_guild.categories:
            if i.name == "Приватные комнаты" or i.name == "Private rooms":
                category = i
                print(i, category)
                is_category = True
                config.category_voice_create = i.id
                for j in i.channels:
                    if j.name.lower() == "настройка-комнаты":
                        config.voice_settings_channel = j.id
                        is_text = True
                        await text_func(i, j)


                    elif j.name.lower() == "создать комнату":
                        config.voice_create_channel = j.id
                        is_voice = True

                break

        if is_text is False and is_voice is False and is_category is False:
            await create(this_guild)
        elif is_voice is False:
            voice_room = await category.create_voice_channel(
                name="Создать комнату")
            config.voice_create_channel = voice_room.id
        elif is_text is False:
            await text_func(category)
