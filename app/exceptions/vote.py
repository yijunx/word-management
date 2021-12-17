class VoteAlreadyExist(Exception):
    status_code = 409

    def __init__(self, user_id: str, version_id: str) -> None:
        self.message = f"User {user_id} already voted for version {version_id}"
        super().__init__(self.message)


class VoteDoesNotExist(Exception):
    status_code = 404

    def __init__(self, user_id: str, version_id: str) -> None:
        self.message = f"User {user_id} has not voted for version {version_id}"
        super().__init__(self.message)
