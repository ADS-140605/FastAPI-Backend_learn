from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published= bool =True
    #rating = Optional[int]=None


@app.get("/")
def root():
    return {"message":"Helloooooooooooooooo"}

@app.get("/posts")
def get_posts():
    return {"data":"These are yout posts"}

@app.post("/createpost")
def create_posts(data : Post):
    print(data.rating)
    return {"new_post":"created"}

