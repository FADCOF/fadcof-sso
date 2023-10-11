# -*- coding: utf-8 -*-
from fastapi import APIRouter
from user.models import User
from fadck.database.base import get_session

router = APIRouter()


@router.get('/')
async def debug():
    with get_session() as sess:
        user = sess.query(User).filter_by(username='saki').first()
        sess.close()
    print(user)
    return {'result': 'hello world!'}
