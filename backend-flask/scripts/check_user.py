import sqlite3
import sys
email = sys.argv[1]
conn = sqlite3.connect('users.db')
cur = conn.cursor()
cur.execute('SELECT email FROM user WHERE email=?', (email,))
r = cur.fetchone()
print(r)
conn.close()
