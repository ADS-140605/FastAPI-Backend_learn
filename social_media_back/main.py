from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

import json
app = FastAPI()

def load_data():
    with open("social_media_dummy.json","r",encoding="utf-8") as file:
        data = json.load(file)

    return data
def dump_data(data):
    with open("social_media_dummy.json","w",encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

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
    return {"data":data}

@app.post("/createpost")
def create_posts(data : Post):
    original_data=load_data()
    original_data.append(data.model_dump())
    dump_data(original_data)
    return {"DATA":data}

