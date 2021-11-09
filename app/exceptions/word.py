class WordDoesNotExist(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class WordAlreadyExist(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)