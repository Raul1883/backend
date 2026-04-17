from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession


from app.db.db import get_async_session
from app.models.orm.models import Character, User
from app.models.schemas.character_schemas import CharacterRead, CharacterCreate, CharacterRequest
from app.services.characters import (
    create_character,
    get_all_characters,
    get_all_my_characters,
    get_character_by_id,
    update_character,
    delete_character,
)
from app.dependencies.auth import MasterUser, get_current_user


router = APIRouter(
    prefix="/characters",
    tags=["Characters"],
)


@router.post("", response_model=CharacterRead, status_code=status.HTTP_201_CREATED)
async def create_character_api(
    character_data: CharacterRequest, 
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        return await create_character(character_data=character_data, user=current_user, session=session)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Foreign key violation: {e}",
        )


@router.get("/all", response_model=List[CharacterRead])
async def get_all_characters_api(
    current_user: MasterUser,
    session: AsyncSession = Depends(get_async_session)
):
    return await get_all_characters(session=session)

@router.get("", response_model=List[CharacterRead])
async def get_all_my_characters_api(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    return await get_all_my_characters(session, current_user)


@router.get("/{character_id}", response_model=CharacterRead)
async def get_character_by_id_api(
    character_id: int, 
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    character = await get_character_by_id(character_id=character_id, session=session, user=current_user)
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found",
        )
    return character


@router.put("/{character_id}", response_model=CharacterRead)
async def update_character_api(
    character_id: int, 
    character_data: CharacterRequest, 
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        return await update_character(
            character_id=character_id, 
            character_data=character_data, 
            user=current_user,
            session=session
        )
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Foreign key violation: {e}",
        )


@router.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_character_api(
    character_id: int, 
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        await delete_character(character_id=character_id, session=session, user=current_user)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Foreign key violation: {e}",
        )
