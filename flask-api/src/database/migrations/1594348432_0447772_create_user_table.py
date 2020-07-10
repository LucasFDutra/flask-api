import migrationsConnection as db
import sys


def up():
    try:
        cursor.execute("""
             CREATE TABLE users (
                id_user_pk TEXT PRIMARY KEY,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)

        connection.commit()
        cursor.close()
        connection.close()
        print('success')
    except:
        print('error')


def down():
    try:
        cursor.execute("DROP TABLE users")

        connection.commit()
        cursor.close()
        connection.close()
        print('success')
    except:
        print('error')


if __name__ == "__main__":
    connection = db.create_db_connection()
    cursor = connection.cursor()

    if ('--up' in sys.argv):
        up()
    elif ('--down' in sys.argv):
        down()
