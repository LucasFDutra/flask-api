import src.database.connection as db


class UserModel():
    def __init__(self):
        self.connection = db.create_db_connection()

    def select_user(self, email: str) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM USERS WHERE email = %s
        """, (email,))
        select_response = cursor.fetchall()

        cursor.close()

        if (len(select_response) > 0):
            return False
        return True

    def create_user(self, id_user: str, email: str, password: str) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO USERS (id_user_pk, email, password) VALUES (%s, %s, %s)
            """, (id_user, email, password))
            self.connection.commit()
            cursor.close()
            return True
        except:
            return False
