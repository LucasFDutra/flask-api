from flask import jsonify
import os
import jwt
import datetime
import re


class AuthController():
    def generate_token(self, id_user: int):
        secretKey = os.environ['FLASK_API_SECRETKEY']
        token = jwt.encode({
            'data': {'id_user': id_user},
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, secretKey, algorithm="HS256")
        return token

    def validate_email(self, email: str):
        regex = r'(^[a-z0-9_.+-]+@[a-z0-9-]+\.[a-z0-9-.]+$)'
        result = re.findall(regex, email)
        if (len(result) < 1 or len(result) > 1):
            return False
        else:
            return (result[0] == email)

    def sigin_user(self):
        token = self.generate_token(12)
        return jsonify({'token': token.decode('UTF-8')}), 200
