import sqlite3

conn = sqlite3.connect('bot_db/bot_db.db', check_same_thread=False)
cursor = conn.cursor()


def addUser(user_id: int, user_FirstName: str, user_LastName: str, user_city: str):
    if user_FirstName is None:
        user_FirstName = 'anonymous first name'
    if user_LastName is None:
        user_LastName = 'anonymous last name'
    cursor.execute('INSERT INTO users (user_id, user_name, user_FirstName, user_LastName, user_city) VALUES (?, ?, ?, '
                   '?, ?)',
                   (user_id, 'username', user_FirstName, user_LastName, user_city))
    conn.commit()


def getUsersFromDB():
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    return rows


