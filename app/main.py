from fastapi import FastAPI, Depends
from .routers import post, user, authentication
from .db.database import engine, Base
from .auth.oauth2 import get_current_active_user
from .db import models

Base.metadata.create_all(bind=engine)

API_DESC = """
### API Server for Posts

By [@theanujdev](https://github.com/theanujdev)
"""

app = FastAPI(
    title="Posts API",
    description=API_DESC,
    version="0.1.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Posts API",
        "url": "https://example.com/",
        # "email": "example@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

app.include_router(authentication.router)
app.include_router(post.router)
app.include_router(user.router)


@app.get("/", name="Root", description="### Base URL", tags=["Default"])
async def root(user: models.User = Depends(get_current_active_user)):
    return {"message": f"Hello {user.username}! Welcome to Posts API server."}
