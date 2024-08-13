import allure
import requests
from conftest import create_user
from data import Url, Endpoints


class TestGetOrderSpecUser:
    @allure.title('Получение списка заказов конкретного авторизованного пользователя')
    def test_get_orders_spec_user_with_auth(self, create_user):
        new_user = create_user
        new_user_log_pass = {
            "email": new_user[0],
            "password": new_user[1]
        }
        response_login = requests.post(f'{Url.URL}{Endpoints.USER_LOGIN}', data=new_user_log_pass)
        token = response_login.json()['accessToken']
        ingredient_1 = "61c0c5a71d1f82001bdaaa6e"
        ingredient_2 = "61c0c5a71d1f82001bdaaa6f"
        ingredients = {"ingredients": [f'{ingredient_1}', f'{ingredient_2}']}
        requests.post(f'{Url.URL}{Endpoints.ORDER_CREATE}', data=ingredients)
        response_order = requests.get(f'{Url.URL}{Endpoints.GET_ORDER_USER}', headers={'Authorization': f'{token}'})
        assert response_order.status_code == 200

    @allure.title('Получение списка заказов конкретного неавторизованного пользователя')
    def test_get_orders_spec_user_without_auth(self, create_user):
        ingredient_1 = "61c0c5a71d1f82001bdaaa73"
        ingredient_2 = "61c0c5a71d1f82001bdaaa6f"
        ingredients = {"ingredients": [f'{ingredient_1}', f'{ingredient_2}']}
        requests.post(f'{Url.URL}{Endpoints.ORDER_CREATE}', data=ingredients)
        response_order = requests.get(f'{Url.URL}{Endpoints.GET_ORDER_USER}')
        assert (response_order.status_code == 401 and
                response_order.text == '{"success":false,"message":"You should be authorised"}')
