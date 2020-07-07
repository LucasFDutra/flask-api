import database.connection as db


class UserModel():
    def __init__(self):
        self.connection = db.create_db_connection()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

        cursor.execute("INSERT INTO test (num, data) VALUES (%s, %s)",
                       (100, "abc'def"))

        self.connection.commit()

        self.connection.close()

        return 'tabela criada com sucesso'
