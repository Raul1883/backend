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


async def create_user(session: AsyncSession, user_data: UserCreate):
    user_data_dump = user_data.model_dump()

    if get_user_by_login(session, user_data_dump["login"]):
        raise UserAlreadyExistsError(user_data_dump["login"])
    
    user_data_dump["hashed_pwd"] = await hash_password(user_data_dump.pop("password"))

    new_user_orm = User(**user_data_dump)

    session.add(new_user_orm)

    await session.commit()
    await session.refresh(new_user_orm)

    return new_user_orm


async def get_all_users(session: AsyncSession):
    result = await session.execute(select(User))

    return result


async def get_user_by_id(session: AsyncSession, user_id: int):
    result = await session.get(User, user_id)

    return result

async def get_user_by_login(session: AsyncSession, login: str):
    stmt = select(User).where(User.login == login)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
