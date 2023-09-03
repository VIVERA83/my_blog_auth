import json


class TestCreateUser:
    def test_ok(self, client, user_data_1):
        """Корректные данные, пользователя с представленным email."""
        response = client.post("auth/create_user", content=json.dumps(user_data_1))
        assert response.status_code == 200
        assert (
            response.json()["message"]
            == f"Sent letter to vivera83@bk.ru, for verification email addresses"
        )
        assert response.json()["detail"] == "OK 200"

    def test_bad_password(self, client, user_data_1):
        """Пароль не сходится."""
        user_data_1["password_confirmation"] = "bad password"
        response = client.post("auth/create_user", content=json.dumps(user_data_1))
        assert response.status_code == 400
        assert response.json()["message"] == "Assertion failed, passwords do not match"
        assert response.json()["detail"] == "400 Bad Request"

    async def test_user_exists(self, user_data_1, client, user_1):
        """Пользователь под представленным email уже зарегистрирован"""

        response = client.post("auth/create_user", content=json.dumps(user_data_1))
        assert response.status_code == 400
        assert (
            response.json()["message"]
            == "Email is already in use, try other email address, not these 'vivera83@bk.ru'"
        )
