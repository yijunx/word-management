from sqlalchemy.sql.expression import and_
from app.casbin.role_definition import ResourceRightsEnum, PolicyTypeEnum
from app.db.models import models
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Tuple
from app.repo.util import translate_query_pagination
from app.schemas.pagination import QueryPagination, ResponsePagination


# def create_policy(
#     db: Session, user_id: str, resource_id: str, resource_right: ResourceRightsEnum
# ) -> models.CasbinRule:
#     """Create only p type here"""
#     db_item = models.CasbinRule(
#         ptype=PolicyTypeEnum.p,
#         v0=user_id,
#         v1=resource_id,
#         v2=resource_right,
#     )
#     db.add(db_item)
#     try:
#         db.flush()
#     except IntegrityError:
#         db.rollback()
#         raise PolicyIsAlreadyThere(
#             user_id=user_id, resource_id=resource_id, resource_right=resource_right
#         )
#     return db_item

def get_all_admin_user_ids(db: Session, admin_role_id: str, query_pagination: QueryPagination) -> Tuple[List[models.CasbinRule], ResponsePagination]:
    query = db.query(models.CasbinRule).filter(
        models.CasbinRule.v1 == admin_role_id
    )
    total = query.count()
    limit, offset, paging = translate_query_pagination(
        query_pagination=query_pagination, total=total
    )

    db_items = query.limit(limit).offset(offset).all()
    paging.page_size = len(db_items)
    return db_items, paging


def delete_policies_by_resource_id(db: Session, resource_id: str) -> None:
    """used when deleting resource"""
    query = db.query(models.CasbinRule).filter(
        and_(
            models.CasbinRule.ptype == PolicyTypeEnum.p,
            models.CasbinRule.v1 == resource_id,
        )
    )
    query.delete()


def delete_policies_by_word_id(db: Session, word_id: str) -> None:
    """used when deleting resource"""
    query = db.query(models.CasbinRule).filter(
        models.CasbinRule.ptype == PolicyTypeEnum.p
    )
    query = query.filter(models.CasbinRule.v1.ilike(f"%{word_id}%"))
    db_items = query.all()
    for db_item in db_items:
        db.delete(db_item)
