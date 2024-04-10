import aiosqlite


async def crate_table():
    async with aiosqlite.connect("rooms.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS rooms_info ("
                         "voice_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                         "voice_name varchar(255) NOT NULL,"
                         "date_created varchar(255) NOT NULL,"
                         "limit_user INTEGER NOT NULL,"
                         "invisible BOOL NOT NULL,"
                         "is_closed BOOL NOT NULL,"
                         "owner_id INTEGER NOT NULL,"
                         "coadministrator_id INTEGER NOT NULL)")
        await db.commit()




