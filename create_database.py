import sqlite3

conn = sqlite3.connect('account.db')
c = conn.cursor()
c.execute('''
CREATE TABLE account
(id INTEGER PRIMARY KEY AUTOINCREMENT,
email TEXT,
storename TEXT,
password TEXT
)
''')
conn.commit()
conn.close()



        


