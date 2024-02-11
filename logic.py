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

    def add_item_to_cart(self, user_id, item_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM cart WHERE user_id = ? and item_id = ?", (user_id, item_id))
            res = cur.fetchall()
            if res:
                cur.execute(
                    "UPDATE cart SET count = count + 1  WHERE user_id = ? AND clothes_id = ? ", (user_id, item_id))
            else:
                cur.execute(
                    "INSERT INTO cart VALUES (?, ?, ?)", (user_id, item_id, 1))
            conn.commit()

    def show_cart(self, user_id):
        pass

    def get_name_of_item(self, clothes_id):
        pass


manager = StoreManager("store.db")
manager.create_tables()
data = [
    ("Кроссовки", 1500, "розовый", "images/sneakers.webp"),
    ("Футболка", 1000, "черный", "images/t-shirt.webp"),
    ("Кепка", 800, "синий", "images/head.jpg")
]
manager.add_items(data)
print(manager.show_items())
