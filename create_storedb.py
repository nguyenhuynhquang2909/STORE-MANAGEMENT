import sqlite3
conn = sqlite3.connect('store.db')
c = conn.cursor()
c.execute('''
CREATE TABLE inventory
(id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
category TEXT,
price REAL,
quantity INTEGER)
''')
conn.commit()
conn.close()