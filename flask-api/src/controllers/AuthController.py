from flask import jsonify
import os
import jwt
import datetime
import re
from src.models.UserModel import UserModel
import uuid


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

    def sign_user(self, data):
        # print(data.headers)
        email = data.headers['EMAIL']
        password = data.headers['PASSWORD']

        # verificar se o email é válido, se não for então retornar que o email é inválido
        if not (self.validate_email(email)):
            return "this email is not a valid email", 400

        # verificar se usuário existe no banco, caso sim, retorna mensagem dizendo que ele já existe
        user_model = UserModel()
        if not (user_model.select_user(email)):
            return "this email already exists", 400

        # se ele não existir, então adicione o mesmo no banco
        id_user = uuid.uuid4().hex

        create_user_response = user_model.create_user(id_user, email, password)

        if not (create_user_response):
            return "Error in create user, try again", 400

        # se tudo deu certo até aqui, então gere o token
        token = self.generate_token(id_user)

        # retorne o token
        return jsonify({'token': token.decode('UTF-8')}), 200
