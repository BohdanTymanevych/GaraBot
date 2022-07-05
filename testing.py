import sqlite3

con = sqlite3.connect("users.db")
c = con.cursor()

all_id = c.execute("SELECT id FROM users").fetchall()
all_id = list(map(lambda x: int(x[0]), all_id))

