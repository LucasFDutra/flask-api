def up(cursor):
    cursor.execute("""
            CREATE TABLE users_2 (
            id_user_pk TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)


def down(cursor):
    cursor.execute("DROP TABLE users_2")
