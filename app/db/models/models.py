from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import UniqueConstraint
from sqlalchemy.sql.sqltypes import BigInteger, Boolean
from .base import Base


class User(Base):
    """User is created via the token in the request cookie"""
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)



class Word(Base):
    __tablename__ = "words"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    locked = Column(String, nullable=False)
    merged_to = Column(String, nullable=True)
    dialect = Column(String, nullable=False)

    created_at = Column(DateTime, nullable=False)
    created_by = Column()  # some foreinkey here

    modified_at = Column(DateTime, nullable=False)
    modified_by = Column() # some foreigkey here
    

class ExplanationVersions(Base):
    __tablename__ = "explanation_versions"

    id = Column(String, primary_key=True, index=True)


class TagVersions(Base):
    __tablename__ = "tag_versions"

    id = Column(String, primary_key=True, index=True)


class UsageVersions(Base):
    __tablename__ = "usage_versions"

    id = Column(String, primary_key=True, index=True)


class PronunciationVersions(Base):
    __tablename__ = "pronunciation_versions"

    id = Column(String, primary_key=True, index=True)


class Suggestions(Base):
    __tablename__ = "suggestions"

    id = Column(String, primary_key=True, index=True)

    

