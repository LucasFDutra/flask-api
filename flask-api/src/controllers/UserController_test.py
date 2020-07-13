from src.controllers.UserController import UserController


def test_generate_token():
    user_controller = UserController()
    print('aqui')
    token = user_controller.generate_token(12)
    print(token)
    assert status == 200
