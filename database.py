import aiosqlite


class VoiceDb():
    def __init__(self):
        self.name = "rooms.db"

    async def crate_table(self):
        async with aiosqlite.connect(self.name) as db:
            c = await db.cursor()
            await c.execute("CREATE TABLE IF NOT EXISTS rooms_info ("
                             "voice_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                             "voice_name varchar(255) NOT NULL,"
                             "date_created TEXT NOT NULL,"
                             "limit_user INTEGER DEFAULT 0,"
                             "invisible BOOL DEFAULT FALSE,"
                             "is_closed BOOL DEFAULT FALSE,"
                             "owner_id INTEGER NOT NULL,"
                             "coadministrator_id INTEGER DEFAULT 0)")
            await db.commit()
            await c.close()


    async def create_room_info(self, voice_i, voice_n, date, owner):
        async with aiosqlite.connect(self.name) as db:
            c = await db.cursor()
            await c.execute(f"INSERT INTO rooms_info "
                             f"(voice_id, voice_name, date_created, owner_id)"
                             f" VALUES ('{voice_i}',"
                             f" '{voice_n}', '{date}', '{owner}')")
            await db.commit()
            await c.close()


    async def remove_room(self, voice_i):
        async with aiosqlite.connect(self.name) as db:
            c = await db.cursor()
            await c.execute(f"DELETE FROM rooms_info WHERE"
                             f" voice_id = '{voice_i}'")
            await db.commit()
            await c.close()


    async def get_user(self, channel_id):
        async with aiosqlite.connect(self.name) as db:
            c = await db.cursor()
            await c.execute(f"SELECT owner_id FROM rooms_info WHERE"
                             f" voice_id = '{channel_id}'")
            res = await c.fetchone()
            print(res)
            await c.close()
            return res

    async def set_voice_name(self, res, channel_id):
        async with aiosqlite.connect(self.name) as db:
            c = await db.cursor()
            await c.execute(f"UPDATE rooms_info SET voice_name = '{res}' where voice_id = '{channel_id}'")
            await db.commit()
            await c.close()

    async def set_limit(self, res, channel_id):
        async with aiosqlite.connect(self.name) as db:
            c = await db.cursor()

            await c.execute(
                f"UPDATE rooms_info SET limit_user = '{res}' WHERE voice_id = {channel_id}")
            await db.commit()
            await c.close()





