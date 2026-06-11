from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import pandas as pd
import json

from requests import status_codes
app = FastAPI()

def load_data():
    with open("social_media_dummy.json","r",encoding="utf-8") as file:
        data = json.load(file)
    return data

def add_col(data,col_name):
    df=pd.DataFrame(data)
    df = df.fillna(value=0)
    df[col_name]=df.get(col_name)
    df["id"] = [f"{i:03}" for i in range(len(df))]
    data=df.to_dict(orient="records")
    return data

def dump_data(data):
    with open("social_media_dummy.json","w",encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
def del_col(data,col_name):
    df=pd.DataFrame(data)
    df = df.drop(columns=col_name)
    data=df.to_dict(orient="records")
    return data
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


@app.get("/")
def root():
    return {"message":"Helloooooooooooooooo"}

@app.get("/posts")
def get_posts():
    data=load_data()
    #data=del_col(data,["id"])
    #data=add_col(data,"id")
    #dump_data(data)
    return {"data":data}

@app.post("/createpost")
def create_posts(data : Post):
    original_data=load_data()
    original_data.append(data.model_dump())
    dump_data(original_data)
    return {"DATA":data}
@app.get("/posts/{id}")
def retrieve_data(id):
    data=load_data()
    for post in data:
        if post.get("id") == id:
            return post

    return {"message": "Post not found"}

@app.delete("/delete/{id}")
def delete_data(id):
    data=load_data()
    for post in data:
        if post.get("id") == id:
            data.remove(post)
            dump_data(data)
            raise HTTPException(status_code=status_codes.HTTP_204_NO_CONTENT, detail="Post deleted successfully")

    return {"message": "Post not found"}

@app.put("/posts/{id}")
def update_data(id,update:Update):
    data=load_data()
    for post in data:
        if post.get("id") == id:
            if update.title is not None:
                post["title"]=update.title
            if update.content is not None:
                post["content"]=update.content
            if update.published is not None:
                post["published"]=update.published
            if update.rating is not None:
                post["rating"]=update.rating
            dump_data(data)
            return {"message":"Post updated successfully"}
    return {"message": "Post not found"}