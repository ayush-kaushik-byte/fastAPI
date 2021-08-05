from fastapi import FastAPI
from repository import models
from database import engine
from routers import user_router, authentication_router,task_router
import uvicorn

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(user_router)
app.include_router(authentication_router)
app.include_router(task_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0",port=5000)