from fastapi import HTTPException, status


class UserException(HTTPException):
    status_code = 400
    detail = ""
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class EmailAlreadyExistsException(UserException):
    status_code=status.HTTP_409_CONFLICT
    detail="Email уже существует"

class UsernamelAlreadyExistsException(UserException):
    status_code=status.HTTP_409_CONFLICT
    detail="Username уже существует"

class IncorrectEmailOrPasswordException(UserException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверная почта или пароль"

class IncorrectTokenFormatException(UserException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверный формат токена"

class TokenAbsentException(UserException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен отсутствует"

class TokenExpiredException(UserException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен истек"

class UserIsNotPresentException(UserException):
    status_code=status.HTTP_401_UNAUTHORIZED
