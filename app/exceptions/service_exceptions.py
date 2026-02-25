class AppException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class UserAlreadyExistsError(AppException):
    def __init__(self, login: str):
        super().__init__(
            message=f"User with login '{login}' already exists",
        )