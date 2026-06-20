from typing import Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import pandas as pd
import json
import os
import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from .database import engine,get_db
from . import model
from sqlalchemy.orm import Session 

model.Base.metadata.create_all(bind=engine)

load_dotenv()

conn = psycopg.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
        row_factory=dict_row
    )



app = FastAPI()

cursor = conn.cursor()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE_PATH = os.path.join(BASE_DIR, "social_media_dummy.json")
def load_data_db():
    cursor.execute("SELECT * FROM posts")
    data = cursor.fetchall()
    return data
while True:
    try:
        data = load_data_db()
        break
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        print("Retrying in 5 seconds...")
        import time
        time.sleep(5)


class Update(BaseModel):
    title: Optional[str]=None
    content: Optional[str]=None
    published: Optional[bool]=None
    rating : Optional[int]=None
class Post(BaseModel):
    title: str
    content: str
    published: bool =True
    rating : Optional[int]=None




@app.get("/sqlalchemy")
def get_sqlalchemy_data(db: Session = Depends(get_db)):
    posts = db.query(model.Post).all()
    return {"data": posts}



@app.get("/")
def root():
    return {"message":"Helloooooooooooooooo"}

@app.get("/posts")
def get_posts():
    data=load_data_db()
    cursor.execute("""SELECT * FROM posts""")
    data=cursor.fetchall()
    print(data)
    #data=del_col(data,["id"])
    #data=add_col(data,"id")
    #dump_data(data)
    return {"data":data}


@app.get("/posts/{id}")
def retrieve_data(id:int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="post not found"
        )
    return post

@app.post("/createpost")
def create_posts(data : Post):
    # original_data=load_data()
    # original_data.append(data.model_dump())
    # dump_data(original_data)
    cursor.execute("""INSERT INTO posts (
                   title,
                   content,
                   published,    
                   rating
                   ) 

                   VALUES 

                   (
                   %s,%s,%s,%s
                   ) RETURNING *
                   """,(data.title, data.content, data.published, data.rating))
    new_post=cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.delete("/delete/{id}")
def delete_data(id: int):
    cursor.execute("""DELETE FROM posts where id=%s returning *""",(str(id),))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Post not found")

    conn.commit()
    return {"message": "Post deleted successfully", "deleted_post": post}


@app.put("/posts/{id}")
def update_data(id: int, update: Update):
    cursor.execute("""SELECT * FROM posts WHERE id=%s""", (str(id),))
    existing_post = cursor.fetchone()
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    cursor.execute(
        """UPDATE posts
           SET title=%s, content=%s, published=%s, rating=%s
           WHERE id=%s
           RETURNING *""",
        (
            update.title if update.title is not None else existing_post["title"],
            update.content if update.content is not None else existing_post["content"],
            update.published if update.published is not None else existing_post["published"],
            update.rating if update.rating is not None else existing_post["rating"],
            str(id),
        ),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    return {"message": "Post updated successfully", "updated_post": updated_post}


