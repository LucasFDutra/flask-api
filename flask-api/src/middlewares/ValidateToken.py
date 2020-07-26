from flask import request, jsonify
import jwt
import os
from functools import wraps


def validate_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        secretKey = os.environ['FLASK_API_SECRETKEY']
        token = request.headers['TOKEN']
        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        try:
            jwt.decode(token, secretKey)
        except:
            return jsonify({'message': 'Token is invalid'}), 403
        return f(*args, **kwargs)
    return decorated
