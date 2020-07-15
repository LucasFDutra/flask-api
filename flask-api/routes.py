from src.controllers.UserController import UserController
from src.controllers.AuthController import AuthController


class Routes():
    def __init__(self):
        self.auth_controller = AuthController()
        self.user_controller = UserController()

    def routes(self, app):
        @app.route('/api/auth/sigin')
        def sigin_user_route():
            return self.auth_controller.sigin_user()
