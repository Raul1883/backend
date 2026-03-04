from app.db.repositories import BaseRepository
from app.exceptions.service_exceptions import UserAlreadyExistsError
import bcrypt

from app.models.orm.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schemas.user_schemas import UserCreate, UserRead


async def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    return hashed_password


async def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
    except ValueError:
        return False

def get_user_repository(session):
    return BaseRepository(session, User)

async def create_user(session: AsyncSession, user_data: UserCreate):
    repository = get_user_repository(session)
    user_data_dump = user_data.model_dump()

    if await get_user_by_login(session, user_data_dump["login"]):
        raise UserAlreadyExistsError(user_data_dump["login"])

    user_data_dump["hashed_pwd"] = await hash_password(user_data_dump.pop("password"))

    return await repository.create(**user_data_dump)


async def get_all_users(session: AsyncSession):
    repository = get_user_repository(session)
    return await repository.get_all()


async def get_user_by_id(session: AsyncSession, user_id: int):
    repository = get_user_repository(session)

    return await repository.get_by_id(user_id)



async def get_user_by_login(session: AsyncSession, login: str):
    stmt = select(User).where(User.login == login)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
