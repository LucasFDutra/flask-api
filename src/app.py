from flask import Flask
from routes import Routes


class App():
    def __init__(self):
        self.app = self.create_app()
        self.routes = Routes()
        self.create_routes(self.app)

    def create_app(self):
        app = Flask(__name__)
        return app

    def get_app(self):
        return self.app

    def create_routes(self, app):
        self.routes.routes(app)
