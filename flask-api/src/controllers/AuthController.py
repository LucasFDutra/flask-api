from flask import jsonify
import os
import jwt
import datetime
import re
from src.models.UserModel import UserModel
import uuid
from hashlib import blake2b
from hmac import compare_digest


class AuthController():
    def generate_token(self, id_user: int) -> bytes:
        secretKey = os.environ['FLASK_API_SECRETKEY']
        token = jwt.encode({
            'data': {'id_user': id_user},
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, secretKey, algorithm="HS256")
        return token

    def validate_email(self, email: str) -> bool:
        regex = r'(^[a-z0-9_.+-]+@[a-z0-9-]+\.[a-z0-9-.]+$)'
        result = re.findall(regex, email)
        if (len(result) < 1 or len(result) > 1):
            return False
        else:
            return (result[0] == email)

    def encrypt_password(self, password):
        SECRETE_KEY_PASSWORD = b'34020230$%$%$108'
        AUTH_SIZE = 16
        h = blake2b(digest_size=AUTH_SIZE, key=SECRETE_KEY_PASSWORD)
        h.update(password.encode())
        string_password = h.hexdigest().encode('utf-8')
        return string_password.decode('utf-8')

    def compare_password(self, password, real_password):
        return self.encrypt_password(password) == real_password

    def sign_user(self, data):
        email = data.headers['EMAIL']
        password = data.headers['PASSWORD']
        password = self.encrypt_password(password)
        print(password)

        if not (self.validate_email(email)):
            return "this email is not a valid email", 400

        user_model = UserModel()
        if (len(user_model.select_user(email)) > 0):
            return "this email already exists", 400

        id_user = uuid.uuid4().hex

        create_user_response = user_model.create_user(id_user, email, password)

        if not (create_user_response):
            return "Error in create user, try again", 400

        token = self.generate_token(id_user)

        return jsonify({'token': token.decode('UTF-8')}), 200

    def login_user(self, data):
        email = data.headers['EMAIL']
        password = data.headers['PASSWORD']

        if not (self.validate_email(email)):
            return "this email is not a valid email", 400

        user_model = UserModel()
        user_model_response = user_model.select_user(email)
        user_model_response_password = user_model_response[0][2]
        user_model_response_id_user = user_model_response[0][1]

        if not (self.compare_password(password, user_model_response_password)):
            return "password incorrect", 400
        token = self.generate_token(user_model_response_id_user)
        return jsonify({'token': token.decode('utf-8')}), 200
