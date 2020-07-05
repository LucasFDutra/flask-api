from flask import Flask, request, jsonify

class UserController():
  def create_user(self):
    return jsonify({'hello_response': 'Hello to user route'})
