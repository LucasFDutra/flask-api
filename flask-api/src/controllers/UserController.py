from flask import jsonify
from src.models.UserModel import UserModel


class UserController():
    def __init__(self):
        self.user_model = UserModel()

    def create_user_table(self):
        status = self.user_model.create_table()
        return jsonify({'ok': status})

    def create_user(self):
        return jsonify({'hello_response': 'Hello to user route'})

    def soma(self, a: int, b: int) -> int:
        return a+b
