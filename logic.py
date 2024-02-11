import sqlite3


class StoreManager:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute("""
						CREATE TABLE IF NOT EXISTS items (
							item_id INTEGER PRIMARY KEY,
							name TEXT NOT NULL,
							price INTEGER NOT NULL,
							color TEXT,
							img TEXT
						)""")

            conn.execute("""
						CREATE TABLE IF NOT EXISTS cart (
							user_id INTEGER,
							item_id INTEGER,
							count INTEGER,
							FOREIGN KEY(item_id) REFERENCES items(item_id)
						)""")
            conn.commit()

    def add_items(self, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(
                "INSERT INTO items (name, price, color, img ) VALUES (?, ?, ?, ?)", data)
            conn.commit()

    def show_items(self):
        conn = sqlite3.connect(self.database)
        cur = conn.cursor()
        cur.execute("SELECT * FROM items")
        result = cur.fetchall()
        return result


manager = StoreManager("store.db")
manager.create_tables()
data = [
    ("Кроссовки", 1500, "розовый", "images/sneakers.webp"),
    ("Футболка", 1000, "черный", "images/t-shirt.webp"),
    ("Кепка", 800, "синий", "images/head.jpg")
]
manager.add_items(data)
print(manager.show_items())
