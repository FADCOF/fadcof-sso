# -*- coding: utf-8 -*-
import httpx
import json
import config
from fastapi import APIRouter, Request
from user import models, schemas
from fadck.database.base import get_session
from fadck.crypto.algo import get_hash_cache

router = APIRouter()

hash_salt = get_hash_cache(config.PASSWORD_HASH_SALT)
hash_store = get_hash_cache(config.PASSWORD_HASH_STORE)

tester = httpx.AsyncClient()


def password_with_salt(username: str, raw_password: str):
    try:
        # Pass raw password is already hashed, hash username as salt.
        salt_bytes = hash_salt.digest(username.encode('utf-8'))
        pass_bytes = bytearray.fromhex(raw_password)
        # Combine the salt with password.
        salted_password = bytearray([0]) * 64
        for ii in range(32):
            salted_password[ii*2] = pass_bytes[ii]
            salted_password[ii*2+1] = salt_bytes[ii]
        # Use SM3 to complete the password encryption.
        return hash_store.digest(salted_password).hex()
    except Exception:
        return ''


@router.post('/user-login')
async def login(user_info: Request):
    # Convert the request into schemas.
    query_info = await user_info.json()
    if 'key' not in query_info or 'user' not in query_info:
        return {'result': 'failed', 'error': 'Incorrect login command.'}
    username = query_info['user']
    password = query_info['key']
    # Query the user.
    query_user = schemas.User(username=username,
                              password=password_with_salt(username, password))
    with get_session() as sess:
        candidate_user = sess.query(models.User).filter_by(
            username=query_user.username,
            password=query_user.password
        ).first()
        sess.close()
    # Create the login status for the candidate users.
    print(candidate_user)
    return {'result': 'ok'}


@router.post('/user-register')
async def register():
    pass


@router.get('/')
async def debug():
    async with httpx.AsyncClient() as client:
        response = await client.post('http://localhost:8000/user-login',
                                     content=json.dumps({'user':'saki','key':hash_salt.digest(b'123').hex()}))
        return {'result': str(response)}
