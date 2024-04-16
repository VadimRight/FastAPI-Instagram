from uuid import uuid4

from asyncpg import NotNullViolationError
from fastapi import HTTPException, Depends
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.oauth import oauth2_scheme
from src.auth.schemas import TokenData
from src.database import get_session
from src.models.models import Post, User
from src.verif import get_id_from_token, verify_owner
from fastapi import UploadFile, File
from src.cassandra_db import *
from PIL import Image
from uuid import UUID

async def create_post(name, text, post_image: UploadFile = File(None), token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    try:
        cassandra_session = cluster.connect('fastapiinstagram')
        user_id = await get_id_from_token(token)
        post_id = uuid4()
        filename = str(post_image.filename)
        id_image = uuid4()
        extenction = filename.split('.')[1]
        if extenction not in ["png", "jpg", "svg"]:
            raise HTTPException(status_code=423, detail = "Inappropriate file type")
        
        generated_name = FILEPATH + str(post_id) + '.' + extenction
        print(generated_name)
        file_content = await post_image.read()
        with open(generated_name, "wb") as file:
            file.write(file_content)

        img = Image.open(generated_name)
        img = img.resize(size = (200, 200))
        user_id = await get_id_from_token(token)
        img.save(generated_name)

        cassandra_session.execute_async(
            f"""
INSERT INTO fastapiinstagram.image (id, item_id, path, user_id) VALUES (%s, %s, %s, %s);
            """,
            (id_image, post_id, generated_name, user_id)
        )
        async with session.begin():
            image = Post(id = post_id, text=text, name=name, user_id=user_id)
            session.add(image)
            await session.flush() 
            await session.refresh(image)
            return f"Post {post_id} is succesfully created"
    except NotNullViolationError:
        raise HTTPException(status_code=400, detail="Please, fill the form properly")
    

async def get_post_by_username(session: AsyncSession, username: str):
    async with session.begin():
        query = select(Post).join(User).where(User.username == username)
        result = await session.execute(query)
        posts = result.scalars()
        if posts == []:
            return {"detail": "User hasn't post anything yet"}
        return (post for post in posts)

    
async def get_post_by_id(session: AsyncSession, id: str):
    cassandra_session = cluster.connect('fastapiinstagram')
    path = cassandra_session.execute_async(
        f"""
    SELECT path FROM fastapiinstagram.image WHERE item_id = %s ALLOW FILTERING;
        """, (UUID(id), ))
    async with session.begin():
        query = select(Post).where(Post.id == id)
        result = await session.execute(query)
        post = result.scalar()
        if post is None:
            raise HTTPException(status_code=400)
        return {"post": post, "path": f"{path.result()[0].path}"}


# TODO: rewrite this function
async def get_username_by_post_id(session: AsyncSession, user_id: str):
        async with session.begin():
            query = select(User.username).where(User.id == Post.user_id)
            result = await session.execute(query)
            username = result.scalar
            if username is None:
                raise HTTPException(status_code=404)
            return username


async def get_my_post(session: AsyncSession, token: str):
    try:
        async with session.begin():
            id = await get_id_from_token(token)
            token_data = TokenData(id=id)
            query = select(Post).join(User).where(User.id == token_data.id)
            result = await session.execute(query)
            my_images = result.scalars()
            if my_images == []:
                return {"detail": "You haven't posted anything yet"}
            return (image for image in my_images)
    except NotNullViolationError:
        raise HTTPException(status_code=400, detail="Please, fill the form properly")


async def delete_my_post(session: AsyncSession, id: str, token: str):
    owner = await verify_owner(session, token, id)
    if owner is False:
        raise HTTPException(status_code=403, detail="You dont have such permission")
    async with session.begin():
        query = delete(Post).where(Post.id == id)
        await session.execute(query)


async def edit_post_name(session: AsyncSession, id: str, name: str, token: str):
    owner = await verify_owner(session, token, id)
    if owner is False:
        raise HTTPException(status_code=403, detail="You dont have such permission")
    async with session.begin():
        query = update(Post).where(Post.id == id).values(name=name)
        await session.execute(query)


async def edit_post_image(session: AsyncSession, id: str, image: str, token: str):
    owner = await verify_owner(session, token, id)
    if owner is False:
        raise HTTPException(status_code=403, detail="You dont have such permission")
    async with session.begin():
        query = update(Post).where(Post.id == id).values(image=image)
        await session.execute(query)
