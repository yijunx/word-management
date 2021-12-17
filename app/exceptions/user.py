class AdminUserDoesNotExist(Exception):
    status_code = 404

    def __init__(self, user_id: str) -> None:
        self.message = f"Admin user {user_id} does not exist"
        super().__init__(self.message)


class AdminUserAlreadyExist(Exception):
    status_code = 409

    def __init__(self, word_title: str, dialect: str) -> None:
        self.message = f"Word {word_title} already exists in dialect {dialect}"
        super().__init__(self.message)
