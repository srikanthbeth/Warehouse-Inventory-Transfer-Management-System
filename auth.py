from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud
import schemas
from auth import create_access_token
from database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# =====================================================
# Register User
# =====================================================

@router.post("/register", response_model=schemas.UserResponse)
def register(
    user: schemas.UserRegister,
    db: Session = Depends(get_db)
):
    return crud.create_user(db, user)


# =====================================================
# Login User
# =====================================================

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = crud.authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role
    }