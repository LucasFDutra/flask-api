import src.database.connection as db


class UserModel():
    def __init__(self):
        self.connection = db.create_db_connection()

    def create_user(self):
        pass
