from flask import jsonify
from src.models.UserModel import UserModel
import jwt
import datetime
import os


class UserController():
    def __init__(self):
        self.user_model = UserModel()
