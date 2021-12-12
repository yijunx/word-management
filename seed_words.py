from app.exceptions.word import WordAlreadyExist
import app.service.word as WordService
from app.schemas.word import DialectEnum, WordCreate
from app.schemas.user import User

INITIAL_WORDS = [
    WordCreate(
        title="62",
        explanation="笨蛋",
        pronunciation="'lo2 er2",
        tags=["笨蛋"],
        usage="个人真当是个62",
        dialect=DialectEnum.hangzhouhua,
    ),
    WordCreate(
        title="介个套",
        explanation="怎么样",
        tags=["怎么样"],
        usage="个件事体介个套",
        dialect=DialectEnum.hangzhouhua,
    ),
    WordCreate(
        title="调羹儿",
        explanation="spoon",
        tags=["勺子"],
        usage="把这个调羹儿给我",
        pronunciation="tiao2 'gang1 er",
        dialect=DialectEnum.hangzhouhua,
    )
]

# add first user
ACTOR = User(
    id="first-user-id",
    name="el psy kongroo",
    email="first-user@dialects.io"
)


def add_initial_words():
    for word in INITIAL_WORDS:
        try:
            WordService.create_word(item_create=word, actor=ACTOR)
        except WordAlreadyExist as e:
            print("exception is:")
            print(e)
            pass


if __name__ == "__main__":
    add_initial_words()
