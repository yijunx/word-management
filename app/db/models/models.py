from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql.schema import ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import BigInteger, Boolean, Integer
from sqlalchemy.orm import relation, relationship
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

    # user is parent to all things below
    words = relationship("Word", back_populates="creator")
    suggestions = relationship("Suggestion", back_populates="creator")
    field_versions = relationship("FieldVersion", back_populates="creator")


class Word(Base):
    __tablename__ = "words"
    __table_args__ = (UniqueConstraint("title", "dialect", name="_title_dialect_uc"),)

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    locked = Column(Boolean, nullable=False)
    merged_to = Column(String, nullable=True)
    dialect = Column(String, nullable=False)

    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)
    created_by = Column(String, ForeignKey("users.id"), nullable=False)

    # User is the parent of this
    creator = relationship("User", back_populates="words")

    # this is the parent of field versions
    field_versions = relationship("FieldVersion", back_populates="word")


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

    # field version is the parant of suggestions
    suggestions = relationship("Suggestion", back_populates="field_version")
    # User is the parent of this
    creator = relationship("User", back_populates="field_versions")
    # word owns it, and no need back polupations
    word = relationship("Word", back_populates="field_versions")


class Suggestion(Base):
    __tablename__ = "suggestions"

    id = Column(String, primary_key=True, index=True)

    word_id = Column(String, ForeignKey("words.id"), nullable=False)
    version_id = Column(String, ForeignKey("field_versions.id"), nullable=False)
    content = Column(String, nullable=False)

    accepted = Column(Boolean, nullable=False)

    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)
    created_by = Column(String, ForeignKey("users.id"), nullable=False)

    # field version is the parant of suggestions
    field_version = relationship("FieldVersion", back_populates="suggestions")
    # User is the parent of this
    creator = relationship("User", back_populates="suggestions")
