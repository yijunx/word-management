from app.schemas.user import User


class NotAuthorized(Exception):
    status_code = 403

    def __init__(self, actor: User, resource_id_or_domain: str, action: str) -> None:
        self.message = f"User {actor.id} has no right to {action} on resource or domain {resource_id_or_domain}"
        super().__init__(self.message)
