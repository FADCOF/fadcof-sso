# -*- coding: utf-8 -*-
from contextlib import asynccontextmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app_ins: FastAPI):
    # Initial the storage.
    from fadck.storage.dir import startup as storage_startup
    storage_startup()
    # Initial the database.
    from fadck.database.base import startup as database_startup
    database_startup()
    # Load the ML model
    yield


app = FastAPI(lifespan=lifespan)
from user.router import router as user_router
app.include_router(user_router)
