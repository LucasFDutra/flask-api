from flask import Flask, request, jsonify
from controllers.UserController import UserController

class Routes():
  def __init__(self):
    self.user_controller = UserController()

  def routes(self, app):
    @app.route('/api')
    def UserControllerRoute():
      return self.user_controller.create_user()


