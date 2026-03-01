from starlette import status


class AppException(Exception):
    def __init__(
        self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class UserAlreadyExistsError(AppException):
    def __init__(self, login: str):
        super().__init__(
            message=f"User with login '{login}' already exists",
            status_code=status.HTTP_409_CONFLICT,
        )


class AttributeAlreadyExistsError(AppException):
    def __init__(self, text: str):
        super().__init__(
            message=f"Attribute with data: '{text}' already exists",
            status_code=status.HTTP_409_CONFLICT,
        )

class AttributeNotFound(AppException):
    def __init__(self, id: str):
        super().__init__(
            message=f"Attribute with id: '{id}' not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

class ForeignKeyViolationError(AppException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        )


