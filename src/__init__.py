from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db, close_db
from src.auth.routes import auth_router
from src.users.router import router
from src.logger import logger

version = "0.1.0"

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()
        yield
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    finally:
        logger.info("Closing connections")
        await close_db()


app = FastAPI(lifespan=lifespan, version=version)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(router, prefix=f"/api/{version}/users")
app.include_router(auth_router, prefix=f"/api/{version}/auth")







