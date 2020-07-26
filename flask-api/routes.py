from flask import request
from src.controllers.UserController import UserController
from src.controllers.AuthController import AuthController
from src.middlewares.ValidateToken import validate_token


class Routes():
    def __init__(self):
        self.auth_controller = AuthController()
        self.user_controller = UserController()

    def routes(self, app):
        @app.route('/api/auth/sign')
        def sign_user_route():
            return self.auth_controller.sign_user(request)

        @app.route('/api/auth/login')
        def login_user_route():
            return self.auth_controller.login_user(request)

        @app.route('/api/user/print')
        @validate_token
        def print_route():
            return self.user_controller.hello(request)
