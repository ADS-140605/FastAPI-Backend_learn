from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
import pandas as pd
import json
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