from flask import jsonify


class UserController():
    def create_user(self):
        return jsonify({'hello_response': 'Hello to user route'})

    def soma(self, a: int, b: int) -> int:
        return a+b
