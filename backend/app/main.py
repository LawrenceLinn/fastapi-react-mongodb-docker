from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from .auth.auth import get_hashed_password
from .config.config import settings
from .models.users import User
from .routers.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup mongoDB
    app.client = AsyncIOMotorClient(
        settings.MONGO_HOST,
        settings.MONGO_PORT,
        username=settings.MONGO_USER,
        password=settings.MONGO_PASSWORD,
    )
    await init_beanie(database=app.client[settings.MONGO_DB], document_models=[User])

    user = await User.find_one({"email": settings.FIRST_SUPERUSER})
    if not user:
        user = User(
            email=settings.FIRST_SUPERUSER,
            hashed_password=get_hashed_password(settings.FIRST_SUPERUSER_PASSWORD),
            is_superuser=True,
        )
        await user.create()

    # yield app
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            # See https://github.com/pydantic/pydantic/issues/7186 for reason of using rstrip
            str(origin).rstrip("/")
            for origin in settings.BACKEND_CORS_ORIGINS
        ],
        # allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.websocket("/ws/video")
async def websocket_video(websocket: WebSocket):
    # print in the console
    print("websocket_video")
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()
        # 对视频数据进行处理
        print("data", data)
        # 这里是处理逻辑的伪代码
        processed_data = process_video_data(data)
        # 将处理后的视频数据发送回客户端
        await websocket.send_bytes(processed_data)


def process_video_data(data):
    # 处理视频数据的伪代码
    return data  # 返回处理后的数据


app.include_router(api_router, prefix=settings.API_V1_STR)
# app.include_router(video.router, prefix="/video")
