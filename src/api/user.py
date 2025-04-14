from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, status
from core.schemas.user import TokenResponse, UserCreate, UserLogin, UserResponse, DummyLogin
from core.db_helper import get_db_connection
from auth.jwt import get_password_hash, verify_password, create_access_token
from uuid import uuid4
from datetime import timedelta

from crud.user import check_user_exists_db, create_user_db, get_user_by_email_db


router = APIRouter(tags=["user"])


@router.post("/dummyLogin", response_model=TokenResponse)
async def dummy_login(
    login_data: DummyLogin,
    conn: Connection = Depends(get_db_connection)
):
    """Эндпоинт Dummy login для тестирования."""
    if login_data.role not in ["employee", "moderator"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role, must be 'employee' or 'moderator'"
        )

    token_data = {
        "sub": str(uuid4()),
        "role": login_data.role
    }
    access_token = create_access_token(
        data=token_data,
        expires_delta=timedelta(minutes=60)
    )
    
    return TokenResponse(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    conn: Connection = Depends(get_db_connection)
):
    """Эндпоинт регистрации нового пользователя."""
    if user_data.role not in ["employee", "moderator"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role, must be 'employee' or 'moderator'"
        )

    hashed_password = get_password_hash(user_data.password)
    
    existing_user = await check_user_exists_db(email=user_data.email, conn=conn)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    new_user = await create_user_db(
        email=user_data.email,
        password_hash=hashed_password,
        role=user_data.role,
        conn=conn
    )

    return new_user

@router.post("/login", response_model=TokenResponse)
async def login_user(
    user_data: UserLogin,
    conn: Connection = Depends(get_db_connection)
):
    """Эндпоинт для входа пользователя."""
    user = await get_user_by_email_db(email=user_data.email, conn=conn)
        
    if not user or not verify_password(user_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = {
        "sub": str(user["id"]),
        "role": user["role"]
    }

    access_token = create_access_token(
        data=token_data,
        expires_delta=timedelta(minutes=60)
    )
    
    return TokenResponse(access_token=access_token, token_type="bearer")