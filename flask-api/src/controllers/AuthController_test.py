from src.controllers.AuthController import AuthController
import os
import jwt
from faker import Faker
from faker.providers import internet
import random
import string

auth_controller = AuthController()
fake = Faker()
fake.add_provider(internet)


def test_generate_token():
    id_user = 12
    token = auth_controller.generate_token(id_user)

    secretKey = os.environ['FLASK_API_SECRETKEY']
    id_user_from_token = jwt.decode(token, secretKey, algorithms=[
                                    'HS256'])['data']['id_user']

    assert (id_user == id_user_from_token)


def test_validate_email_correct():
    for i in range(15):
        email = fake.ascii_email()
        response = auth_controller.validate_email(email)
        assert (response == True)


def test_validate_email_error():
    email_list = [
        "bri@ttany90@henry.com",
        "rcar*ey@ya!hoo.com",
        "jacobdickso#n@edwards.com",
        "mçartincassandra@gmail.com",
        "$elee@zamora.com",
        "p%%%ricechristopher@schmidt.net",
        "jenn&%iferelliott@ferguson.biz",
        "jonesa()ngela@hotmail.com",
        "xmarquezjohnson-andrews.info",
        "samuel35@gAESmail.com",
        "hooperangeDASla@smith.info",
        "andrewbrooks@moores%@#ruiz.com",
        "andrewbrookésmoores@ruiz.com"
    ]
    for email in email_list:
        response = auth_controller.validate_email(email)
        print(response, email)
        assert response == False


def test_encrypt_password():
    letters = string.ascii_letters + string.digits + \
        string.printable + string.punctuation
    password = ''.join([random.choice(letters) for i in range(16)])
    encrypted_password = auth_controller.encrypt_password(password)
    assert len(encrypted_password) > 0


def test_compare_password_correct():
    letters = string.ascii_letters + string.digits + \
        string.printable + string.punctuation
    password = ''.join([random.choice(letters) for i in range(16)])
    encrypted_password = auth_controller.encrypt_password(password)
    assert auth_controller.compare_password(password, encrypted_password)


def test_compare_password_error():
    letters = string.ascii_letters + string.digits + \
        string.printable + string.punctuation
    password_1 = ''.join([random.choice(letters) for i in range(16)])
    password_2 = ''.join([random.choice(letters) for i in range(16)])
    encrypted_password = auth_controller.encrypt_password(password_1)
    assert not auth_controller.compare_password(password_2, encrypted_password)


# def test_sign_user():
#     email = fake.ascii_email()
#     res = auth_controller.sign_user(email, '1234')
#     print(res)
#     secretKey = os.environ['FLASK_API_SECRETKEY']
#     id_user_from_token = jwt.decode(token, secretKey, algorithms=[
#         'HS256'])['data']['id_user']
#     assert status == 200
