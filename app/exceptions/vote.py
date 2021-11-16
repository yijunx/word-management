class VoteAlreadyExist(Exception):
    def __init__(self, user_id: str, version_id: str) -> None:
        self.http_code = 409
        self.message = f"User {user_id} already voted for version {version_id}"
        super().__init__(self.message)


class VoteDoesNotExist(Exception):
    def __init__(self, user_id: str, version_id: str) -> None:
        self.http_code = 404
        self.message = f"User {user_id} has not voted for version {version_id}"
        super().__init__(self.message)
