from disnake.ext import commands
import aiosqlite
import datetime
import random

from config import category_id, voice_create_id

import pytz


class VoiceDb(commands.Cog):
    def __init__(self):
        self.name = "db/voice.db"

    async def create_table(self):
        async with aiosqlite.connect(self.name) as db:
            c = await db.cursor()

            await c.execute(
                "CREATE TABLE if not EXISTS voice ("
                "channel_id INTEGER PRIMARY KEY,"
                "channel_name TEXT NOT NULL,"
                "date_created TEXT NOT NULL,"
                "user TEXT NOT NULL,"
                "limit_user INTEGER NOT NULL,"
                "invisible BOOL NOT NULL,"
                "is_closed BOOL NOT NULL)"
            )

            await db.commit()

    async def delete_string(self, channel_id):
        async with aiosqlite.connect(self.name) as db:
            c = await db.cursor()

            await c.execute(
                f"DELETE FROM voice WHERE channel_id = {channel_id}")
            await db.commit()

    async def add_create_channel(self, channel_id, channel_name, date_created,
                                 user, limit_user):
        async with aiosqlite.connect(self.name) as db:
            c = await db.cursor()

            await c.execute(
                f"INSERT INTO voice (channel_id, channel_name, date_created, user, limit_user, invisible, is_closed) "
                f"VALUES ('{channel_id}', '{channel_name}', '{date_created}', '{user}', "
                f"'{limit_user}', '{None}', '{None}')")

            await db.commit()

    async def update_isClosed(self, values, channel_id):
        async with aiosqlite.connect(self.name) as db:
            c = await db.cursor()

            await c.execute(
                f"UPDATE voice SET is_closed = '{values}' WHERE channel_id = {channel_id}")
            await db.commit()

    async def update_invisible(self, values, channel_id):
        async with aiosqlite.connect(self.name) as db:
            c = await db.cursor()

            await c.execute(
                f"UPDATE voice SET invisible = '{values}' WHERE channel_id = {channel_id}")
            await db.commit()

    async def set_limit(self, res, channel_id):
        async with aiosqlite.connect(self.name) as db:
            c = await db.cursor()

            await c.execute(
                f"UPDATE voice SET limit_user = '{res}' WHERE channel_id = {channel_id}")
            await db.commit()

    async def set_voice_name(self, res, channel_id):
        async with aiosqlite.connect(self.name) as db:
            c = await db.cursor()

            await c.execute(
                f"UPDATE voice SET channel_name = '{res}' WHERE channel_id = {channel_id}")
            await db.commit()

    async def get_isClosed(self, channel_id):
        async with aiosqlite.connect(self.name) as db:
            c = await db.cursor()

            await c.execute(
                f"SELECT is_closed FROM voice WHERE channel_id = '{channel_id}'")
            is_closed = (await c.fetchone())[0]
            if is_closed != "None":
                is_closed = eval(is_closed)
                return is_closed
            return None

    async def get_isInvisible(self, channel_id):
        async with aiosqlite.connect(self.name) as db:
            c = await db.cursor()

            await c.execute(
                f"SELECT invisible FROM voice WHERE channel_id = '{channel_id}'")
            invisible = (await c.fetchone())[0]
            if invisible != "None":
                invisible = eval(invisible)
                return invisible
            return None

    async def change_user_name(self, res, channel_id):
        async with aiosqlite.connect(self.name) as db:
            c = await db.cursor()

            await c.execute(
                f"UPDATE voice SET user = '{res}' WHERE channel_id = '{channel_id}'")
            await db.commit()

    async def get_user(self, channel_id):
        async with aiosqlite.connect(self.name) as db:
            c = await db.cursor()

            await c.execute(
                f"SELECT user FROM voice WHERE channel_id = '{channel_id}'")
            user = (await c.fetchone())[0]

            return user

    async def create_channel(self, member, new_channel, voice_db):

        moscow_tz = pytz.timezone('Europe/Moscow')
        now_moscow = datetime.datetime.now().astimezone(moscow_tz)
        await voice_db.add_create_channel(channel_id=new_channel.id,
                                          channel_name=new_channel.name,
                                          date_created=now_moscow.strftime(
                                              "%d-%m-%Y %H:%M:%S"),
                                          user=member.mention,
                                          limit_user=new_channel.user_limit)

    async def delete_voice(self, member, before):
        try:
            if before.channel.category.id == category_id and before.channel.id != voice_create_id:
                if len(before.channel.members) == 0:
                    await before.channel.delete()
                    await VoiceDb().delete_string(before.channel.id)
                else:
                    a = await VoiceDb().get_user(before.channel.id)
                    if member.display_name == a:
                        members = before.channel.members
                        ran_member = random.choice(members)
                        await VoiceDb().change_user_name(
                            ran_member.display_name, before.channel.id)
            else:
                pass
        except:
            pass

    async def info(self, channel_id):
        async with aiosqlite.connect(self.name) as db:
            c = await db.cursor()

            await c.execute(
                f"SELECT * FROM voice WHERE channel_id = '{channel_id}'")
            res = await c.fetchall()

            return res
