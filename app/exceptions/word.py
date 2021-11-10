class WordDoesNotExist(Exception):
    def __init__(self, word_id: str) -> None:
        self.http_code = 404
        self.message = f"Word {word_id} does not exist"
        super().__init__(self.message)


class WordAlreadyExist(Exception):
    def __init__(self, word_title: str) -> None:
        self.http_code = 409
        self.message = f"Word {word_title} already exists"
        super().__init__(self.message)