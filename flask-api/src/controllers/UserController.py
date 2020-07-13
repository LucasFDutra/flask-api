from flask import jsonify
from src.models.UserModel import UserModel
import jwt
import datetime
import os


class UserController():
    def __init__(self):
        self.user_model = UserModel()

    def generate_token(self, id_user):
        secretKey = os.environ['FLASK_API_SECRETKEY']
        token = jwt.encode({
            'data': id_user,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, secretKey)
        return jsonify({'token': token.decode('UTF-8')})

    def create_user(self):
        return jsonify({'hello_response': 'Hello to user route'}), 200
