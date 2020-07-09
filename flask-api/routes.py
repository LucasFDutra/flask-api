from src.controllers.UserController import UserController


class Routes():
    def __init__(self):
        self.user_controller = UserController()

    def routes(self, app):
        @app.route('/api')
        def create_user_route():
            return self.user_controller.create_user()

        @app.route('/api/create')
        def create_user_table_route():
            return self.user_controller.create_user_table()
