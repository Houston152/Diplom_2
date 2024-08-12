import allure
import pytest
import requests
from conftest import create_user
from data import Url, Endpoints
from faker import Faker

fake = Faker("ru_RU")


class TestUserLogin:
    @allure.title('Успешная авторизация пользователя')
    def test_success_auth(self, create_user):
        new_user = create_user
        new_user_log_pass = {
            "email": new_user[0],
            "password": new_user[1]
        }
        response = requests.post(f'{Url.URL}{Endpoints.USER_LOGIN}', data=new_user_log_pass)
        access_token = response.json()['accessToken']
        refresh_token = response.json()['refreshToken']
        email = response.json()['user']['email']
        name = response.json()['user']['name']
        assert response.text == (f'{{"success":true,"accessToken":"{access_token}","refreshToken":"{refresh_token}",'
                                 f'"user":{{"email":"{email}","name":"{name}"}}}}')

    @allure.title('Авторизация пользователя с неверным логином или паролем')
    @pytest.mark.parametrize("email, password", [
        (fake.ascii_free_email(), ""),
        ("", fake.password())
    ])
    def test_auth_with_invalid_credentials(self, create_user, email, password):
        new_user = create_user
        user_with_incorrect_credentials = {
            "email": email or new_user[0],
            "password": password or new_user[1]
        }
        response = requests.post(f'{Url.URL}{Endpoints.USER_LOGIN}', data=user_with_incorrect_credentials)
        assert (response.status_code == 401 and
                response.text == '{"success":false,"message":"email or password are incorrect"}')
