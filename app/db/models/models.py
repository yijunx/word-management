from enum import unique
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import BigInteger, Boolean, Integer
from sqlalchemy.orm import relationship
from .base import Base


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

    




