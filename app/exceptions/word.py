class WordDoesNotExist(Exception):
    status_code = 404

    def __init__(self, word_id: str) -> None:
        self.message = f"Word {word_id} does not exist"
        super().__init__(self.message)


class WordAlreadyExist(Exception):
    status_code = 409

    def __init__(self, word_title: str, dialect: str) -> None:
        self.message = f"Word {word_title} already exists in dialect {dialect}"
        super().__init__(self.message)


class TagDoesNotExist(Exception):
    status_code = 404

    def __init__(self, tag: str) -> None:
        self.message = f"Tag {tag} does not exist"
        super().__init__(self.message)
