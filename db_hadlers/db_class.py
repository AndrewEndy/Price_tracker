import aiosqlite
import asyncio

class DatabaseBot:

    def __init__(self, db_file):
        self.db_file = db_file
        self.lock = asyncio.Lock()
        

    async def __aenter__(self):
        self.db = await aiosqlite.connect(self.db_file)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.db.close()
        
        
    async def on_start_up(self):

        await self.db.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                telegram_id INTEGER PRIMARY KEY NOT NULL,
                username TEXT NOT NULL
            )''')
        
        await self.db.execute('''
            CREATE TABLE IF NOT EXISTS Products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                url TEXT NOT NULL,
                name TEXT NOT NULL,
                price REAL,
                min_price REAL,
                max_price REAL
            )''')
        
        await self.db.commit()
        

    async def check_user(self, telegram_id: int):
        async with self.lock:
            async with self.db.execute("SELECT telegram_id FROM Users WHERE telegram_id = ?", (telegram_id,)) as cursor:
                user_exist = await cursor.fetchone()
                return bool(user_exist)
            
    
    async def add_user(self, telegram_id: int, username: str):
        async with self.lock:
            await self.db.execute("INSERT INTO Users (telegram_id, username) VALUES (?, ?)", (telegram_id, username))
            await self.db.commit()
