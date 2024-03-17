import select
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import ALGORITHM, SECRET
from src.models.models import Image, User



async def get_id_from_token(token: str):
    payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    id: int = payload.get("sub")
    return id


async def verify_user(session: AsyncSession, token: str, id) -> bool:
    async with session.begin():
        user_id = await get_id_from_token(token)
        query = select(User.id).where(User.id == id)
        result = await session.execute(query)
        owner_id = result.scalar()
        return owner_id == user_id


async def verify_owner(session: AsyncSession, token: str, image_id) -> bool:
    async with session.begin():
        user_id = await get_id_from_token(token)
        query = select(Image.user_id).where(Image.id == image_id)
        result = await session.execute(query)
        owner_id = result.scalar()
        return owner_id == user_id
