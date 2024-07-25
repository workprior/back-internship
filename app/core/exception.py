class UserNotFoundError(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id


class EmailUserNotFoundError(Exception):
    def __init__(self, email: str):
        self.email = email


class UserEmailAlreadyExistsError(Exception):
    def __init__(self, email: str):
        self.email = email


class UserPhoneAlreadyExistsError(Exception):
    def __init__(self, phone: str):
        self.phone = phone
