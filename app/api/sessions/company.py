from fastapi import APIRouter, HTTPException, Depends, status, Request
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import get_async_session
from app.db.repositories import BaseRepository
from app.exceptions.service_exceptions import ForeignKeyViolationError
from app.models.orm.models import Company, Genre, System
from app.models.schemas.session_schemas import CompanySchema, CreateCompanySchema, ShortCompanySchema
from app.models.schemas.user_schemas import UserRead, UserCreate

from app.services import user
from app.services import sessions
from app.exceptions.service_exceptions import AttributeAlreadyExistsError


router = APIRouter(
    tags=["Company"],
)


@router.post(
    "/company",
    response_model=CompanySchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_company(
    company: CreateCompanySchema,
    session: AsyncSession = Depends(get_async_session),
):
    return await sessions.create_attribute(session, Company, company)


@router.get(
    "/company", response_model=List[CompanySchema], status_code=status.HTTP_200_OK
)
async def get_all_companies(
    session: AsyncSession = Depends(get_async_session),
):
    return await sessions.get_all_attributes(session, Company)


@router.get(
    "/company_short",
    response_model=List[ShortCompanySchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_companies_short(
    session: AsyncSession = Depends(get_async_session),
):
    result = await sessions.get_all_attributes(session, Company)
    response = [ShortCompanySchema(id=x.id, text=x.title) for x in result]
    return response


@router.get(
    "/company/{company_id}",
    response_model=CompanySchema,
    status_code=status.HTTP_200_OK,
)
async def get_company_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await sessions.get_attribute_by_id(session, Company, id)


@router.delete("/company/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(id: int, session: AsyncSession = Depends(get_async_session)):
    await sessions.delete_attribute(session, Company, id)
