import allure
import requests
import pytest
from conftest import create_user
from data import Url, Endpoints
from faker import Faker

fake = Faker("ru_RU")


class TestUserDataUpdate:

    @pytest.mark.parametrize("update_type", [
        "email",
        "password"
    ])
    @allure.title('Обновление данных пользователя с авторизацией')
    def test_update_user_data_with_auth(self, create_user, update_type):
        new_user = create_user
        new_user_log_pass = {
            "email": new_user[0],
            "password": new_user[1]
        }
        response = requests.post(f'{Url.URL}{Endpoints.USER_LOGIN}', data=new_user_log_pass)
        token = response.json()['accessToken']
        if update_type == "email":
            update_user_data = {
                "email": fake.ascii_free_email(),
                "password": new_user[1]
            }
        else:
            update_user_data = {
                "email": new_user[0],
                "password": fake.password()
            }
        response_update = requests.patch(f'{Url.URL}{Endpoints.USER_DATA_UPDATE}',
                                         headers={'Authorization': f'{token}'},
                                         data=update_user_data)
        email = response_update.json().get('user', {}).get('email')
        name = response_update.json().get('user', {}).get('name')
        assert response_update.text == f'{{"success":true,"user":{{"email":"{email}","name":"{name}"}}}}'

    @pytest.mark.parametrize("update_type", [
        "email",
        "password"
    ])
    @allure.title('Обновление данных пользователя без авторизации')
    def test_update_user_data_without_auth(self, create_user, update_type):
        new_user = create_user
        if update_type == "email":
            update_user_data = {
                "email": new_user[0],
                "password": fake.password()
            }
        else:
            update_user_data = {
                "email": fake.ascii_free_email(),
                "password": new_user[1]
            }

        response = requests.patch(f'{Url.URL}{Endpoints.USER_DATA_UPDATE}', data=update_user_data)
        assert (response.status_code == 401 and
                response.text == '{"success":false,"message":"You should be authorised"}')
