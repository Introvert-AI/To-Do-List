from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import semua router
from API.APIACCOUNT import router as task_router
from API.APICOMMENT import router as comment_router
from API.APITASK import router as like_router
from API.APILIKE import router as account_router
from API.APITASK2 import router as other_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_router)
app.include_router(account_router)
app.include_router(like_router)
app.include_router(comment_router)
app.include_router(other_router)

@app.get("/")
def root():
    return {"message": "API is running!"}