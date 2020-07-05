from flask import Flask, request, jsonify
from routes import Routes
import os

class App():
  def __init__(self):
    self.app = self.create_app()
    self.define_env()
    self.routes = Routes()
    self.create_routes(self.app)

  def create_app(self):
    app = Flask(__name__)
    return app

  def get_app(self):
    return self.app

  def define_env(self):
    os.environ['FLASK_ENV'] = 'development'

  def create_routes(self, app):
    self.routes.routes(app)
