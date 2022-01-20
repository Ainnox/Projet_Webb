import sqlite3
import bcrypt

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())
cur = connection.cursor()

cur.execute("INSERT INTO Posts (title_post, content_post) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO Posts (title_post, content_post) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

cur.execute("INSERT INTO Rights (rights_name) VALUES ('edit'),"
            "('create'),"
            "('delete');")

cur.execute("INSERT INTO Role (role_name) VALUES ('admin'),"
            "('modo'),"
            "('writer'),"
            "('guest');")

cur.execute("INSERT INTO Posses VALUES (1,1),"
            "(1,2),"
            "(1,3),"
            "(2,3),"
            "(3,2),"
            "(3,1);")

cur.execute(
    "INSERT INTO Events (title_event,content_event,event_date) "
    "VALUES ('UFO encounter','On va voir des aliens','2020-02-12')")

salt = bcrypt.gensalt(rounds=10)
hashed = bcrypt.hashpw("admin".encode('utf-8'), salt)
admin = [
    "admin@admin.com",
    "admin",
    hashed,
    1
]

cur.execute("INSERT INTO Users VALUES(?,?,?,?)", admin)
connection.commit()
connection.close()
