from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routes.user import router as UserRouter
from routes.post import router as PostRouter
from routes.comment import router as CommentRouter
from routes.relationship import router as RelationshipRouter
from routes.chat import router as ChatRouter
from routes.room import router as RoomRouter
from db.redis import redis_cache

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def startup_db_client():
    await redis_cache.init_cache()
    # value = await redis_cache.keys('*')
    # await redis_cache.set("boss", "trungtin")
    # messages = await redis_cache.xread(['test'], timeout=60000)
    # print(messages)


@app.on_event("shutdown")
async def shutdown_db_client():
    await redis_cache.close()


@app.get("/", tags=["Root"], response_class=HTMLResponse)
async def read_root() -> dict:
    return """
    <html>
        <head>
            <title>TinySM | FastAPI</title>
        </head>
        <body>
            <h1 style="text-align: center">Gotcha! Browse to <a href="/docs">/docs</a> for details!</h1>
        </body>
    </html>
    """

app.include_router(UserRouter, tags=["User"], prefix="/auth")
app.include_router(PostRouter, tags=["Post"], prefix="/post")
app.include_router(CommentRouter, tags=["Comment"], prefix="/comment")
app.include_router(RelationshipRouter, tags=["Relationship"], prefix="/relationship")
app.include_router(ChatRouter, tags=["Chat"], prefix="/chat")
app.include_router(RoomRouter, tags=["Room"], prefix="/room")


