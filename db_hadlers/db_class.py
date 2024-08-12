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
        '''Метод який, при старті бота, створює таблиці в бд'''

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
                store_name TEXT,
                price REAL,
                min_price REAL,
                max_price REAL,
                state TEXT,
                currency TEXT
            )''')
        
        await self.db.commit()
        

    async def check_user(self, telegram_id: int):
        '''Метод який перевіряє чи є користувач в бд'''
        async with self.lock:
            async with self.db.execute("SELECT telegram_id FROM Users WHERE telegram_id = ?", (telegram_id,)) as cursor:
                user_exist = await cursor.fetchone()
                return bool(user_exist)
            
    
    async def add_user(self, telegram_id: int, username: str):
        '''Метод який додає нового користувача в бд'''
        async with self.lock:
            await self.db.execute("INSERT INTO Users (telegram_id, username) VALUES (?, ?)", (telegram_id, username))
            await self.db.commit()
            
    
    async def get_products(self, telegram_id: int):
        '''Метод для отримання всіх товарів користувача'''
        async with self.lock:
            async with self.db.execute("SELECT * FROM Products WHERE telegram_id = ?", (telegram_id,)) as cursor:
                products = await cursor.fetchall()
                return products # [(id, tg_id, URL, name, store_name, price, min_price, max_price, state, currency)]
    
    
    async def get_product_by_product_id(self, product_id: int, telegram_id: int):
        '''Метод для отримання товара по id'''
        async with self.lock:
            async with self.db.execute("SELECT * FROM Products WHERE telegram_id = ? AND id = ?", (telegram_id, product_id)) as cursor:
                products = await cursor.fetchall()
                return products
        
    
    async def set_product(self, telegram_id: int, url: str ,name: str, store_name: str, price: float, max_price: float, currency: str, state: str):
        '''Метод для встановлення даних про товар'''
        async with self.lock:
            await self.db.execute('''
                INSERT INTO Products (telegram_id, url, name, store_name, price, min_price, max_price, currency, state) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (telegram_id, url, name, store_name, price, price, max_price, currency, state))  # Вставка з однаковим значенням для price і min_price
            await self.db.commit()


    async def update_product_name(self, telegram_id: int, old_name: str, new_name: str):
        '''Метод для зміни назви товара'''
        async with self.lock:
            await self.db.execute('''
                UPDATE Products 
                SET name = ?
                WHERE name == ? AND telegram_id == ?
            ''', (new_name, old_name, telegram_id))
            await self.db.commit()
        
        
    async def check_similar_url(self, telegram_id: int ,url: str):
        '''Метод перевіряє чи є вже такий товар в користувача'''
        async with self.lock:
            async with self.db.execute("SELECT * FROM Products WHERE telegram_id == ? AND url == ?", (telegram_id, url)) as cursor:
                products = await cursor.fetchall()
                if products:
                    return True
                return False
