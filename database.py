import aiosqlite


async def crate_table():
    async with aiosqlite.connect("rooms.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS rooms_info ("
                         "voice_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                         "voice_name varchar(255) NOT NULL,"
                         "date_created TEXT NOT NULL,"
                         "limit_user INTEGER DEFAULT 0,"
                         "invisible BOOL DEFAULT FALSE,"
                         "is_closed BOOL DEFAULT FALSE,"
                         "owner_id INTEGER NOT NULL,"
                         "coadministrator_id INTEGER DEFAULT 0)")
        await db.commit()


async def create_room_info(voice_i, voice_n, date, owner):
    async with aiosqlite.connect("rooms.db") as db:
        await db.execute(f"INSERT INTO rooms_info "
                         f"(voice_id, voice_name, date_created, owner_id)"
                         f" VALUES ('{voice_i}',"
                         f" '{voice_n}', '{date}', '{owner}')")
        await db.commit()


async def remove_room(voice_i):
    async with aiosqlite.connect("rooms.db") as db:
        await db.execute(f"DELETE FROM rooms_info WHERE voice_id = '{voice_i}'")
        await db.commit()




