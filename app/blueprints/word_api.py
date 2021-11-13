from flask import Blueprint, request
from flask_pydantic import validate
from app.casbin.role_definition import ResourceDomainEnum, ResourceActionsEnum
from app.schemas.word import WordQueryByTitle