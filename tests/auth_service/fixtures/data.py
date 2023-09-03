import pytest
from sqlalchemy import insert, text
from store.user.models import UserModel


@pytest.fixture(scope="function")
def user_data_1() -> dict:
    return {
        "password": "password",
        "password_confirmation": "password",
        "name": "Aleksey",
        "email": "vivera83@bk.ru",
    }


@pytest.fixture(scope="function")
async def user_1(db) -> UserModel:
    async with db.begin().session as session:
        query = insert(UserModel).values(
            **{"password": "password", "name": "Aleksey", "email": "vivera83@bk.ru"}
        )
        result = await session.execute(query.returning(UserModel))
        await session.commit()
        return result.scalar_one_or_none()
