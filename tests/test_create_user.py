import pytest
import allure
import requests
from conftest import create_user, create_user_response
from data import Url, Endpoints
from faker import Faker

fake = Faker("ru_RU")


class TestCreateUser:
    @allure.title('Проверка, что пользователь успешно регистрируется')
    def test_create_new_user(self, create_user_response):
        user = create_user_response
        email = user.json()['user']['email']
        name = user.json()['user']['name']
        access_token = user.json()['accessToken']
        refresh_token = user.json()['refreshToken']
        assert user.text == (f'{{"success":true,"user":{{"email":"{email}","name":"{name}"}},'
                             f'"accessToken":"{access_token}","refreshToken":"{refresh_token}"}}')

    @allure.title('Создание пользователя, который уже существует')
    def test_create_existing_user(self, create_user):
        new_user = create_user
        create_existing_user = {
            "email": new_user[0],
            "password": new_user[1],
            "name": new_user[2]
        }
        response = requests.post(f'{Url.URL}{Endpoints.USER_REGISTRATION}', data=create_existing_user)
        assert response.status_code == 403 and response.text == '{"success":false,"message":"User already exists"}'

    @allure.title('Создание пользователя без заполнения обязательного поля email, пароля или имени')
    @pytest.mark.parametrize('email, password, name', [
        ['', fake.password(), fake.first_name()],
        [fake.ascii_free_email(), '', fake.first_name()],
        [fake.ascii_free_email(), fake.password(), '']
    ])
    def test_create_user_without_log_or_pass_or_name(self, email, password, name):
        user_without_log_or_pass_or_name = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(f'{Url.URL}{Endpoints.USER_REGISTRATION}', data=user_without_log_or_pass_or_name)
        assert (response.status_code == 403 and
                response.text == '{"success":false,"message":"Email, password and name are required fields"}')
