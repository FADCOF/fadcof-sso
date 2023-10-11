# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy import event

from fadck.database.base import Base


class ModifyRecordBase(Base):
    __abstract__ = True
    time_create = Column(DateTime, default=datetime.utcnow())
    time_last_modify = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())


@event.listens_for(ModifyRecordBase, 'before_update')
def before_modify_record_update(mapper, connection, target):
    target.time_last_modify = datetime.utcnow()


@event.listens_for(ModifyRecordBase, 'before_insert')
def before_modify_record_insert(mapper, connection, target):
    current_time = datetime.utcnow()
    target.time_last_modify = current_time
    target.time_create = current_time


class UserRole(ModifyRecordBase):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)


class User(ModifyRecordBase):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, default='')
    is_active = Column(Boolean, default=True)


class UserBelongs(ModifyRecordBase):
    __tablename__ = "user_belong"
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('user_roles.id'), primary_key=True)
