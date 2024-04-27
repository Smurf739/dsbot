import datetime

from disnake.ext import commands
from disnake.interactions import MessageInteraction
import disnake

from config import voice_create_id, category_id, message_settings_id
import config
from utils.helper import in_voice, is_leader
from utils.functions import get_time_now, get_info
from database.roomsdb import VoiceDb

mychannel = None


class VoiceButtons(disnake.ui.View):
    def __init__(self):
        self.voice_db = VoiceDb()
        super().__init__(timeout=None)

    @disnake.ui.button(style=disnake.ButtonStyle.secondary, emoji="👥",
                       custom_id="people")
    @in_voice
    @is_leader
    async def room1_settings(self, message,
                             interaction: disnake.MessageInteraction):
        await interaction.response.send_modal(
            ModalHandler(interaction.user.voice.channel,
                         interaction.user.voice.channel.id, "limit"))


    @disnake.ui.button(style=disnake.ButtonStyle.secondary, emoji="🔒",
                       custom_id="lock")
    @in_voice
    @is_leader
    async def room2_settings(self, message,
                             interaction: disnake.MessageInteraction):
        permission = interaction.user.voice.channel.overwrites_for(
            interaction.guild.default_role).connect
        invisible = await self.voice_db.get_isInvisible(
            channel_id=interaction.user.voice.channel.id)
        if permission or permission is None:
            await interaction.user.voice.channel.set_permissions(
                interaction.guild.default_role, connect=False,
                view_channel=invisible)
            await self.voice_db.update_isClosed(False,
                                                interaction.user.voice.channel.id)
            await interaction.response.send_message(embed=disnake.Embed(
                title=f"📦 Комната: {interaction.user.voice.channel.mention}",
                description="**Закрыть/открыть комнату**",
                color=0x2f3136
            ).add_field(name="",
                        value=f"> {interaction.author.mention}, ваша комната закрыта").set_footer(
                text=f"Сегодня, в {get_time_now()}").set_thumbnail(
                interaction.author.avatar),
                                                    ephemeral=True)

        else:
            await interaction.user.voice.channel.set_permissions(
                interaction.guild.default_role, connect=True,
                view_channel=invisible)
            await self.voice_db.update_isClosed(True,
                                                interaction.user.voice.channel.id)

            await interaction.response.send_message(embed=disnake.Embed(
                title=f"📦 Комната: {interaction.user.voice.channel.mention}",
                description="**Закрыть/открыть комнату**",
                color=0x2f3136
            ).add_field(name="",
                        value=f"> {interaction.author.mention}, ваша комната открыта").set_footer(
                text=f"Сегодня, в {get_time_now()}").set_thumbnail(
                interaction.author.avatar),
                                                    ephemeral=True)

    @disnake.ui.button(style=disnake.ButtonStyle.secondary, emoji="👑",
                       custom_id="crown")
    @in_voice
    @is_leader
    async def room4_settings(self, message,
                             interaction: disnake.MessageInteraction):
        view = disnake.ui.View(timeout=None)
        view.add_item(UserSelect("owner", interaction))

        await interaction.response.send_message(embed=disnake.Embed(
            title="Передать владельца",
            description=f"> **{interaction.author.mention}**, выбери пользователя, которому хочешь передать **владельца**:",
            color=0x2f3136
        ).set_footer(
            text=f"Сегодня, в {get_time_now()}").set_thumbnail(
            interaction.author.avatar), view=view,
                                                ephemeral=True)

    @disnake.ui.button(style=disnake.ButtonStyle.secondary, emoji="🤐",
                       custom_id="sound")
    @in_voice
    @is_leader
    async def room5_settings(self, message,
                             interaction: disnake.MessageInteraction):
        view = disnake.ui.View(timeout=None)
        view.add_item(UserSelect("mute", interaction))

        await interaction.response.send_message(embed=disnake.Embed(
            title="Замутить/размутить пользователя",
            description=f"> **{interaction.author.mention}**, выбери пользователя, которого хочешь замутить/размутить:",
            color=0x2f3136
        ).set_footer(text=f"Сегодня, в {get_time_now()}").set_thumbnail(
            interaction.author.avatar), view=view,
                                                ephemeral=True)

    @disnake.ui.button(style=disnake.ButtonStyle.secondary, emoji="✏️",
                       custom_id="voice_name")
    @in_voice
    @is_leader
    async def room6_settings(self, message,
                             interaction: disnake.MessageInteraction):
        await interaction.response.send_modal(
            ModalHandler(interaction.user.voice.channel,
                         interaction.user.voice.channel.id, "voice_name"))

    @disnake.ui.button(style=disnake.ButtonStyle.secondary, emoji="📔",
                       custom_id="user_perm")
    @in_voice
    @is_leader
    async def room8_settings(self, message,
                             interaction: disnake.MessageInteraction):
        view = disnake.ui.View(timeout=None)
        view.add_item(UserSelect("add", interaction))

        await interaction.response.send_message(embed=disnake.Embed(
            title="Добавить/убрать права на подключение",
            description=f"> **{interaction.author.mention}**, выбери пользователя, которому хочешь **дать/забрать** доступ к каналу:",
            color=0x2f3136
        ).set_footer(text=f"Сегодня, в {get_time_now()}").set_thumbnail(
            interaction.author.avatar), view=view,
                                                ephemeral=True)

    @disnake.ui.button(style=disnake.ButtonStyle.secondary, emoji="🦵",
                       custom_id="kick")
    @in_voice
    @is_leader
    async def room9_settings(self, message,
                             interaction: disnake.MessageInteraction):
        view = disnake.ui.View(timeout=None)
        view.add_item(UserSelect("kick", interaction))

        await interaction.response.send_message(embed=disnake.Embed(
            title="Кикнуть пользователя",
            description=f"> **{interaction.author.mention}**, выбери пользователя, которого хочешь **кикнуть**:",
            color=0x2f3136
        ).set_footer(text=f"Сегодня, в {get_time_now()}").set_thumbnail(
            interaction.author.avatar), view=view,
                                                ephemeral=True)

    @disnake.ui.button(emoji="🕵🏻", style=disnake.ButtonStyle.secondary,
                       custom_id="hide")
    @in_voice
    @is_leader
    async def room10_settings(self, message,
                              interaction: disnake.MessageInteraction):
        channel = interaction.user.voice.channel
        permission = channel.overwrites_for(
            interaction.guild.default_role).view_channel
        is_closed = await self.voice_db.get_isClosed(channel.id)
        if permission or permission is None:
            await channel.set_permissions(interaction.guild.default_role,
                                          overwrite=disnake.PermissionOverwrite(
                                              view_channel=False,
                                              connect=is_closed))
            await self.voice_db.update_invisible(False, channel.id)

            await interaction.response.send_message(embed=disnake.Embed(
                title=f"📦 Комната: {interaction.user.voice.channel.mention}",
                description="**Скрыть/показать комнату**",
                color=0x2f3136
            ).add_field(name="",
                        value=f"> {interaction.author.mention}, ваша комната скрыта").set_footer(
                text=f"Сегодня, в {get_time_now()}").set_thumbnail(
                interaction.author.avatar),
                                                    ephemeral=True)
        else:
            await channel.set_permissions(interaction.guild.default_role,
                                          overwrite=disnake.PermissionOverwrite(
                                              view_channel=True,
                                              connect=is_closed))
            await self.voice_db.update_invisible(True, channel.id)

            await interaction.response.send_message(embed=disnake.Embed(
                title=f"📦 Комната: {interaction.user.voice.channel.mention}",
                description="**Скрыть/показать комнату**",
                color=0x2f3136
            ).add_field(name="",
                        value=f"> {interaction.author.mention}, ваша комната видна").set_footer(
                text=f"Сегодня, в {get_time_now()}").set_thumbnail(
                interaction.author.avatar),
                                                    ephemeral=True)

    @disnake.ui.button(emoji="🔄", style=disnake.ButtonStyle.secondary,
                       custom_id="reload")
    @in_voice
    @is_leader
    async def room11_settings(self, message,
                              interaction: disnake.MessageInteraction):
        view = disnake.ui.View(timeout=None)
        view.add_item(UserSelect("reload", interaction))

        await interaction.response.send_message(embed=disnake.Embed(
            title="Сбросить права",
            description=f"> **{interaction.author.mention}**, выберите пользователя, которому хочешь **сбросить** права:",
            color=0x2f3136
        ).set_footer(text=f"Сегодня, в {get_time_now()}").set_thumbnail(
            interaction.author.avatar), view=view, ephemeral=True)

    @disnake.ui.button(emoji="ℹ️", style=disnake.ButtonStyle.secondary,
                       custom_id="info")
    @in_voice
    async def room12_settings(self, message,
                              interaction: disnake.MessageInteraction):
        channel = interaction.user.voice.channel
        res = await self.voice_db.info(channel.id)
        res = list(res[0])

        isClosed_value = "Открытый для всех" if res[6] == "None" or res[
            6] == "True" else "Закрытый для всех"
        invisible_value = "Виден для всех" if res[5] == "None" or res[
            5] == "True" else "Скрыт для всех"
        embed = get_info(channel, res, interaction, isClosed_value,
                         invisible_value)
        await interaction.response.send_message(embed=embed, ephemeral=True)


class UserSelect(disnake.ui.UserSelect):
    def __init__(self, *args):
        self.args = args
        self.voice_db = VoiceDb()
        self.interaction = args[1]
        super().__init__(placeholder="Выбери пользователя",
                         custom_id="UserSelect",
                         min_values=0,
                         max_values=1)

    async def callback(self, interaction: MessageInteraction):
        if interaction.values is None:
            interaction.response.defer()
        else:
            message = await self.interaction.original_response()
            if self.args[0] == "owner":
                user = interaction.guild.get_member(int(interaction.values[0]))
                if user != interaction.user:
                    if user.display_name in [i.display_name for i in
                                             interaction.user.voice.channel.members]:
                        guild = interaction.guild
                        await self.voice_db.change_user_name(user.display_name,
                                                             interaction.user.voice.channel.id)

                        await message.edit(embed=disnake.Embed(
                            title=f"📦 Комната: {interaction.user.voice.channel.mention}",
                            description="**Смена владельца комнаты**",
                            color=0x2f3136
                        ).add_field(name="",
                                    value=f"> Владелец комнаты изменён с {interaction.user.mention} "
                                          f"на {user.mention}").set_footer(
                            text=f"Сегодня, в {get_time_now()}").set_thumbnail(
                            interaction.author.avatar),
                                           view=None)

                        await interaction.user.voice.channel.set_permissions(
                            user, overwrite=None)
                        await user.move_to(interaction.user.voice.channel)
                    else:
                        await message.edit(
                            embed=disnake.Embed(
                                title="Ошибка",
                                description=f"❌ | {interaction.author.mention}, данного учатсника нет в комнате",
                                color=0x2f3136).set_footer(
                                text=f"Сегодня, в {get_time_now()}"),
                            view=None)
                else:
                    await message.edit(
                        embed=disnake.Embed(
                            title="Ошибка",
                            description=f"❌ | {interaction.author.mention}, нельзя выдать права самому себе",
                            color=0x2f3136).set_footer(
                            text=f"Сегодня, в {get_time_now()}"), view=None)

            elif self.args[0] == "add":
                user = interaction.guild.get_member(int(interaction.values[0]))
                if user != interaction.user:
                    if interaction.user.voice.channel.overwrites_for(
                            user).connect is False:
                        await interaction.user.voice.channel.set_permissions(
                            user, connect=True)

                        await message.edit(embed=disnake.Embed(
                            title=f"📦 Комната: {interaction.user.voice.channel.mention}",
                            description="**Выдача прав к каналу**",
                            color=0x2f3136
                        ).add_field(name="",
                                    value=f"> Вы выдали пользователю {user.mention} доступ к каналу").set_footer(
                            text=f"Сегодня, в {get_time_now()}").set_thumbnail(
                            interaction.author.avatar),
                                           view=None)
                    else:
                        await interaction.user.voice.channel.set_permissions(
                            user, connect=False)
                        await message.edit(embed=disnake.Embed(
                            title=f"📦 Комната: {interaction.user.voice.channel.mention}",
                            description="**Выдача прав к каналу**",
                            color=0x2f3136
                        ).add_field(name="",
                                    value=f"> Вы забрали у пользователя {user.mention} доступ к каналу").set_footer(
                            text=f"Сегодня, в {get_time_now()}").set_thumbnail(
                            interaction.author.avatar),
                                           view=None)
                        if user.voice.channel == interaction.user.voice.channel:
                            await user.move_to(None)
                else:

                    await message.edit(
                        embed=disnake.Embed(
                            title="Ошибка",
                            description=f"❌ | {interaction.author.mention}, нельзя забрать у  себя права",
                            color=0x2f3136).set_footer(
                            text=f"Сегодня, в {get_time_now()}"), view=None)

            elif self.args[0] == "mute":
                user = interaction.guild.get_member(int(interaction.values[0]))
                if user != interaction.user:
                    if int(interaction.values[0]) in [i.id for i in
                                                      interaction.user.voice.channel.members]:
                        channel = interaction.user.voice.channel
                        if channel.overwrites_for(
                                user).speak is True or channel.overwrites_for(
                                user).speak == None:
                            await channel.set_permissions(user, speak=False)

                            await user.move_to(interaction.user.voice.channel)

                            await message.edit(embed=disnake.Embed(
                                title=f"📦 Комната: {interaction.user.voice.channel.mention}",
                                description="**размут пользователя**",
                                color=0x2f3136
                            ).add_field(name="",
                                        value=f"> Пользователь {user.mention} замучен").set_footer(
                                text=f"Сегодня, в {get_time_now()}").set_thumbnail(
                                interaction.author.avatar),
                                               view=None)

                        else:
                            await channel.set_permissions(user, speak=True)
                            await user.move_to(interaction.user.voice.channel)
                            await message.edit(embed=disnake.Embed(
                                title=f"📦 Комната: {interaction.user.voice.channel.mention}",
                                description="**Мут/размут пользователя**",
                                color=0x2f3136
                            ).add_field(name="",
                                        value=f"> Пользователь {user.mention} размучен").set_footer(
                                text=f"Сегодня, в {get_time_now()}").set_thumbnail(
                                interaction.author.avatar),
                                               view=None)
                    else:
                        await message.edit(
                            embed=disnake.Embed(
                                title="Ошибка",
                                description=f"❌ | {interaction.author.mention}, данного учатсника нет в комнате",
                                color=0x2f3136).set_footer(
                                text=f"Сегодня, в {get_time_now()}"),
                            view=None)
                else:
                    await message.edit(
                        embed=disnake.Embed(
                            title="Ошибка",
                            description=f"❌ | {interaction.author.mention}, нельзя замутить себя",
                            color=0x2f3136).set_footer(
                            text=f"Сегодня, в {get_time_now()}"), view=None)



            elif self.args[0] == "kick":
                user = interaction.guild.get_member(int(interaction.values[0]))
                if user != interaction.user:
                    if int(interaction.values[0]) in [i.id for i in
                                                      interaction.user.voice.channel.members]:
                        await user.move_to(None)

                        await message.edit(embed=disnake.Embed(
                            title=f"📦 Комната: {interaction.user.voice.channel.mention}",
                            description="**Кик с комнаты**",
                            color=0x2f3136
                        ).add_field(name="",
                                    value=f"> Пользователь {user.mention} был кикнуть с вашего канала").set_footer(
                            text=f"Сегодня, в {get_time_now()}").set_thumbnail(
                            interaction.author.avatar),
                                           view=None)
                    else:
                        await message.edit(
                            embed=disnake.Embed(
                                title="Ошибка",
                                description=f"❌ |{interaction.author.mention}, данного учатсника нет в комнате",
                                color=0x2f3136).set_footer(
                                text=f"Сегодня, в {get_time_now()}"),
                            view=None)
                else:
                    await message.edit(
                        embed=disnake.Embed(
                            title="Ошибка",
                            description=f"❌ |{interaction.author.mention}, нельзя кикнуть себя",
                            color=0x2f3136).set_footer(
                            text=f"Сегодня, в {get_time_now()}"), view=None)


            elif self.args[0] == "reload":
                user = interaction.guild.get_member(int(interaction.values[0]))
                channel = interaction.user.voice.channel
                await channel.set_permissions(user, overwrite=None)
                await user.move_to(interaction.user.voice.channel)

                await message.edit(embed=disnake.Embed(
                    title=f"📦 Комната: {interaction.user.voice.channel.mention}",
                    description="**Ты успешно отредактировал свою комнату!**",
                    color=0x2f3136
                ).add_field(name="",
                            value=f"> Права пользователя {user.mention} были сброшены").set_footer(
                    text=f"Сегодня, в {get_time_now()}").set_thumbnail(
                    interaction.author.avatar),
                                   view=None)


class ModalHandler(disnake.ui.Modal):
    def __init__(self, channel, channel_id, arg):
        self.channel = channel
        self.channel_id = channel_id
        self.voicedb = VoiceDb()
        self.arg = arg

        if self.arg == "voice_name":
            label = "Укажи название войса."
            custom_id = "voice_name"
            placeholder = ""
            title = "Изменение названия войса"
        elif self.arg == "limit":
            label = "Укажи лимит."
            custom_id = "limit"
            placeholder = "Укажи количество участников от 0 до 99"
            title = "Изменение названия войса"
        components = [
            disnake.ui.TextInput(label=label, placeholder=placeholder,
                                 custom_id=custom_id)
        ]
        super().__init__(title=title, custom_id=custom_id,
                         components=components)

    async def callback(self, interaction: disnake.MessageInteraction) -> None:
        if interaction.text_values is None:
            interaction.response.defer()
        else:
            if self.arg == "voice_name":
                last_name = self.channel.name
                res = interaction.text_values["voice_name"]
                await self.channel.edit(name=res)
                await self.voicedb.set_voice_name(res, self.channel_id)

                await interaction.response.send_message(embed=disnake.Embed(
                    title=f"📦 Комната: {interaction.user.voice.channel.mention}",
                    description="**Ты успешно отредактировал свою комнату!**",
                    color=0x2f3136
                ).add_field(name="",
                            value=f"> {interaction.author.mention},"
                                  f" название комнаты изменено с {last_name} на {res}").set_footer(
                    text=f"Сегодня, в {get_time_now()}").set_thumbnail(
                    interaction.author.avatar),
                                                        ephemeral=True)

            elif self.arg == "limit":
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
                ).add_field(name="",
                            value=f"> {interaction.author.mention}, новый лимит пользователей - **{res}**").set_footer(
                    text=f"Сегодня, в {get_time_now()}").set_thumbnail(
                    interaction.author.avatar),
                                                        ephemeral=True)


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voicedb = VoiceDb()
        self.persistents_views_added = False

    @commands.command(name="настроить")
    async def setting(self, ctx):
        await self.voicedb.create_table()
        embed = disnake.Embed(title="📦 Настройка комнаты",
                              description="Выбери подходящие кнопки, чтобы настроить свою руму",
                              color=0x313338)

        embed.add_field(name="",
                        value="<:__:1128033585262243931> — установить лимит\n"
                              "<:__:1128033651855200366> — закрыть/открыть комнату\n"
                              "<:doorkey:1128033580589797508> — забрать/выдать доступ к руме\n"
                              "<:__:1128033698059649116> — передать владельца\n"
                              "<:__:1128033671287406632> — забрать/выдать право говорить")
        embed.add_field(name="",
                        value="<:__:1128033654753468416> — сменить название\n"
                              "<:use:1128033582435270756> — выгнать из комнаты\n"
                              "<:eye:1128033646775902270> — скрыть/открыть комнату\n"
                              "<:repeat:1128033683383779390> — сбросить права пользователя\n"
                              "<:file:1128033650131337286> — информация о комнате")
        embed.set_footer(text="Использовать можно только в голосовом канале")

        await ctx.send(embed=embed, view=VoiceButtons())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        global mychannel
        from config import voice_create_id
        try:
            print(voice_create_id)
            if after.channel.id == voice_create_id:
                mychannel = await after.channel.category.create_voice_channel(
                    name=member.name
                )
                date_created = datetime.datetime.now().strftime(
                    "%y years %m month %d days %H hours %M minutes %S seconds")
                print(type(date_created))
                print(date_created)
                await member.move_to(mychannel)
                await VoiceDb().create_channel(member, mychannel, self.voicedb)

        except AttributeError:
            if before.channel == mychannel:
                if len(before.channel.members) == 0:
                    await self.voicedb.delete_voice(member, before)
            else:
                pass
        print(before.channel, mychannel)
        if before.channel == mychannel:
            if len(before.channel.members) == 0:
                await before.channel.delete()
                await self.voicedb.delete_voice(member, before)
        else:
            pass

    @commands.Cog.listener()
    async def on_connect(self):
        if self.persistents_views_added:
            return
        await self.voicedb.create_table()
        self.bot.add_view(VoiceButtons(), message_id=message_settings_id)


async def text_func(category=None, settings_room=None):
    if settings_room is None:
        settings_room = await category.create_text_channel(
            name="Настройка "
                 "комнаты")
        config.message_settings_id = settings_room.id
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
    config.category_id = category.id

    settings_room = await category.create_text_channel(
        name="Настройка "
             "комнаты")

    voice_room = await category.create_voice_channel(
        name="Создать комнату")
    config.message_settings_id = settings_room.id
    config.voice_create_id = voice_room.id

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
                        config.message_settings_id = j.id
                        is_text = True
                        await text_func(i, j)


                    elif j.name.lower() == "создать комнату":
                        config.voice_create_id = j.id
                        is_voice = True

                break

        if is_text is False and is_voice is False and is_category is False:
            await create(this_guild)
        elif is_voice is False:
            voice_room = await category.create_voice_channel(
                name="Создать комнату")
            config.voice_create_id = voice_room.id
        elif is_text is False:
            await text_func(category)


def setup(bot):
    bot.add_cog(Voice(bot))
