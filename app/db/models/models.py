from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql.schema import ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import BigInteger, Boolean, Integer
from sqlalchemy.orm import relationship
from .base import Base


class CasbinRule(Base):
    __tablename__ = "casbin_rule"
    __table_args__ = (UniqueConstraint("v0", "v1", name="_v0_v1_uc"),)
    id = Column(BigInteger, autoincrement=True, primary_key=True, index=True)
    ptype = Column(String, nullable=False)
    v0 = Column(String, nullable=True)
    v1 = Column(String, nullable=True)
    v2 = Column(String, nullable=True)
    v3 = Column(String, nullable=True)
    v4 = Column(String, nullable=True)
    v5 = Column(String, nullable=True)


class User(Base):
    """User is created via the token in the request cookie"""

    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)

    # we can add more things here like if the user's email has been verified
    # however the authen will reject him if email not verified..


class Word(Base):
    __tablename__ = "words"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False, unique=True)
    locked = Column(Boolean, nullable=False)
    merged_to = Column(String, nullable=True)
    dialect = Column(String, nullable=False)

    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)
    created_by = Column(String, ForeignKey("users.id"), nullable=False)

    # well here i dont want to add any relation.. it could be very messy
    # need to use aio something to fetch the right field versions


class FieldVersion(Base):
    __tablename__ = "field_versions"

    id = Column(String, primary_key=True, index=True)
    word_id = Column(String, ForeignKey("words.id"), nullable=False)
    # explanation|usage|pronounciation|tag
    field = Column(String, nullable=False)
    content = Column(String, nullable=False)

    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)
    created_by = Column(String, ForeignKey("users.id"), nullable=False)

    up_votes = Column(Integer, nullable=False)
    down_votes = Column(Integer, nullable=False)

    suggestions = relationship("Suggestion", back_populates="field_version")


class Suggestion(Base):
    __tablename__ = "suggestions"

    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)
    created_by = Column(String, ForeignKey("users.id"), nullable=False)
    word_id = Column(String, ForeignKey("words.id"), nullable=False)
    version_id = Column(String, ForeignKey("field_versions.id"), nullable=False)

    content = Column(String, nullable=False)
    accepted = Column(Boolean, nullable=False)
    
    field_version = relationship("FieldVersion", back_populates="suggestions")
