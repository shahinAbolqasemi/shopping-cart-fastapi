from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.cart import router as cart_router
from app.routers.users import router as users_router
from app.config import get_settings
from app.utils import get_logger
from app.db import init_db

settings = get_settings()
logger = get_logger(__name__)
app = FastAPI(
    title='Cart API',
    version='1.0.0',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[],
    max_age=3600
)


@app.on_event("startup")
async def startup():
    logger.info("Starting up application")
    init_db()


@app.get("/")
async def root():
    return {"message": f"Check health of the API"}


app.include_router(cart_router, prefix=settings.cart_path_prefix + "/cart")
app.include_router(users_router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)
