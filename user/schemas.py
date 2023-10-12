# -*- coding: utf-8 -*-
from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    email: str | None = None
    is_active: bool = True


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    username: str
    id: int
    is_active: bool = True


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreateRequest(BaseModel):
    username: str
    password: str
    email: str


class UserRoleCreateRequest(BaseModel):
    name: str


class UserPermissionAssignRequest(BaseModel):
    user_id: int
    role_id: int
