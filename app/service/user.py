import app.repo.user as UserRepo
from app.db.database import get_db


def delete_user(item_id):
    with get_db() as db:
        UserRepo.delete(db=db, item_id=item_id)
