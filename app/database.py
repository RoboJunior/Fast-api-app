from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import psycopg2
from psycopg2.extras import  RealDictCursor
import os
from config import get_settings, Config


SQLALCHEMY_DATABASE = Config.DB_CONFIG.format(get_settings().DATABASE_USERNAME,
                                              get_settings().DATABASE_PASSWORD, 
                                              get_settings().DATABASE_HOSTNAME, 
                                              get_settings().DATABASE_NAME)

engine = create_engine(SQLALCHEMY_DATABASE)

Sessionlocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi',user='postgres', password='jeya2001', cursor_factory=RealDictCursor)
#         curr = conn.cursor()
#         print("Database Connected Successfully ...")
#         break
#     except Exception as e:
#         print(f"Error connecting to Database : {e}")
#         time.sleep(2)