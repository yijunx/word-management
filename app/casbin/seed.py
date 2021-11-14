from app.schemas.user import User
from datetime import datetime, timezone
from app.db.database import get_db
import app.repo.user as userRepo
import os


def seed_or_get_admin_user() -> str:

    name = os.getenv("ADMIN_USER_NAME")
    email = os.getenv("ADMIN_USER_EMAIL")
    id = os.getenv("ADMIN_USER_ID")
    actor=User(
                id=id,
                name=name,
                email=email
            )

    with get_db() as db:
        userRepo.get_or_create(
            db=db, actor=actor
        )
    return actor.id