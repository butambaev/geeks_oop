import sqlite3
conn = sqlite3.connect('videogames.db')
cursor = conn.cursor()

# Таблица игр
cursor.execute('''
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    genre TEXT,
    price REAL,
    in_stock INTEGER
)
''')

# Таблица покупателей
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT
)
''')

# Таблица заказов
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    game_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (game_id) REFERENCES games(id)
)
''')

conn.commit()

# Игры
cursor.executemany('''
INSERT INTO games (name, genre, price, in_stock) VALUES (?, ?, ?, ?)
''', [
    ("Cyberpunk 2077", "RPG", 59.99, 10),
    ("The Witcher 3", "RPG", 39.99, 5),
    ("Among Us", "Party", 4.99, 20),
    ("Minecraft", "Sandbox", 26.95, 15)
])

# покупатели
cursor.executemany('''
INSERT INTO customers (name, email) VALUES (?, ?)
''', [
    ("Alice", "alice@mail.com"),
    ("Bob", "bob@mail.com")
])

# заказы
cursor.executemany('''
INSERT INTO orders (customer_id, game_id, quantity) VALUES (?, ?, ?)
''', [
    (1, 1, 1), 
    (1, 3, 2),  
    (2, 2, 1)  
])

conn.commit()
 
cursor.execute('''
SELECT name FROM customers
WHERE id IN (
    SELECT customer_id FROM orders
    JOIN games ON orders.game_id = games.id
    WHERE games.price > 50
)
''')
print(cursor.fetchall())

cursor.execute('''
SELECT customers.name, SUM(games.price * orders.quantity) AS total_spent
FROM orders
JOIN customers ON orders.customer_id = customers.id
JOIN games ON orders.game_id = games.id
GROUP BY customers.name
''')
print(cursor.fetchall())

cursor.execute('''
CREATE VIEW IF NOT EXISTS order_summary AS
SELECT orders.id AS order_id, customers.name AS customer, games.name AS game, quantity, games.price
FROM orders
JOIN customers ON orders.customer_id = customers.id
JOIN games ON orders.game_id = games.id
''')

cursor.execute('SELECT * FROM order_summary')
print(cursor.fetchall())

conn.close()
