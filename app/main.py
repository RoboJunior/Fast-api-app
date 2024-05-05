from fastapi import FastAPI
import psycopg2
from psycopg2.extras import  RealDictCursor
import time
from . import models
from .database import engine
from .routers import post,user,auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',user='postgres', password='jeya2001', cursor_factory=RealDictCursor)
        curr = conn.cursor()
        print("Database Connected Successfully ...")
        break
    except Exception as e:
        print(f"Error connecting to Database : {e}")
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"hello": "world"}





