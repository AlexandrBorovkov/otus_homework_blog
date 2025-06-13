from fastapi import HTTPException, status


class PostException(HTTPException):
    status_code = 400
    detail = ""
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class PostAlreadyExistsException(PostException):
    status_code=status.HTTP_409_CONFLICT
    detail="Пост уже существует"

class PostWasNotFoundException(PostException):
    status_code=status.HTTP_409_CONFLICT
    detail="Такой пост не найден"

class RestrictionOnUpdatingPostException(PostException):
    status_code=status.HTTP_409_CONFLICT
    detail="У вас нет прав на обновление"

class RestrictionOnDeletingPostException(PostException):
    status_code=status.HTTP_409_CONFLICT
    detail="У вас нет прав на удаление"
