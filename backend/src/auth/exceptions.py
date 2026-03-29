class UserNotFoundException(Exception):
    """Raised when user is not found."""

    def __init__(self, user_id: int = None, email: str = None):
        self.user_id = user_id
        self.email = email
        if user_id:
            super().__init__(f"User with id {user_id} not found")
        elif email:
            super().__init__(f"User with email {email} not found")
        else:
            super().__init__("User not found")


class InvalidCredentialsException(Exception):
    """Raised when credentials are invalid."""

    def __init__(self):
        super().__init__("Invalid email or password")


class UserAlreadyExistsException(Exception):
    """Raised when user with email already exists."""

    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email {email} already exists")


class InactiveUserException(Exception):
    """Raised when user is inactive."""

    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email {email} is inactive")