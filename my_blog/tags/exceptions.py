from fastapi import HTTPException, status


class TagException(HTTPException):
    status_code = 400
    detail = ""
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class TagAlreadyExistsException(TagException):
    status_code=status.HTTP_409_CONFLICT
    detail="Тег уже существует"

class TagWasNotFoundException(TagException):
    status_code=status.HTTP_409_CONFLICT
    detail="Такой тег не найден"

class TheTagIsUsedException(TagException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Тег используется в постах"
