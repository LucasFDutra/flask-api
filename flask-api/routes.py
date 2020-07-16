from flask import request
from src.controllers.UserController import UserController
from src.controllers.AuthController import AuthController


class Routes():
    def __init__(self):
        self.auth_controller = AuthController()
        self.user_controller = UserController()

    def routes(self, app):
        @app.route('/api/auth/sign')
        def sign_user_route():
            return self.auth_controller.sign_user(request)
