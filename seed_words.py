import app.service.word as WordService
from app.schemas.word import WordCreate
from app.schemas.user import User

INITIAL_WORDS = [

]
ACTOR = User()
def main():
    WordService.create_word(item_create="lol", actor="lol")


if __name__ == "__main__":
    main()