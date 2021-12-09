import app.service.word as WordService
from app.schemas.word import WordCreate
from app.schemas.user import User

INITIAL_WORDS = [
    WordCreate(),
    WordCreate(),
    WordCreate(),
    WordCreate(),
    WordCreate(),
    WordCreate(),
    WordCreate(),
    WordCreate(),
    WordCreate(),
]
ACTOR = User()
def main():
    for word in INITIAL_WORDS:
        try:
            WordService.create_word(item_create=word, actor=ACTOR)
        except:
            pass

if __name__ == "__main__":
    main()