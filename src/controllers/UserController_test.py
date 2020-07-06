from src.controllers.UserController import UserController


def test_soma():
    user_controller = UserController()
    assert user_controller.soma(1, 2) == 3
    assert user_controller.soma('aba', 'cate') == 'abacate'
