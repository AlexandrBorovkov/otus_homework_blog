from fastapi import APIRouter, Form, Request, Response
from fastapi.responses import RedirectResponse

from my_blog.templates import templates
from my_blog.users.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from my_blog.users.dao import UserDAO
from my_blog.users.exceptions import (
    EmailAlreadyExistsException,
    IncorrectEmailOrPasswordException,
    UsernamelAlreadyExistsException,
)
from my_blog.users.schemas import SUser, SUserLogin

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"])


@router.get("/register")
async def show_register_form(request: Request):
    return templates.TemplateResponse(
        "auth/register.html",
        {"request": request}
    )

@router.post("/register")
async def register_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    existing_user = await UserDAO.find_one_or_none(email=email)
    if existing_user:
        raise EmailAlreadyExistsException
    existing_user = await UserDAO.find_one_or_none(username=username)
    if existing_user:
        raise UsernamelAlreadyExistsException
    hashed_password = get_password_hash(password)
    await UserDAO.add(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    return RedirectResponse(url="/auth/login", status_code=303)

@router.get("/login")
async def show_login_form(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@router.post("/login")
async def login_user(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
):
    user = await authenticate_user(email, password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie("user_access_token", access_token, httponly=True)
    return response

@router.post("/logout")
async def logout_user(response: Response):
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("user_access_token")
    return response
