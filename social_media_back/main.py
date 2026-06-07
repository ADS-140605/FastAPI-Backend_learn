from fastapi import FastAPI
from fastapi.params import Body
app = FastAPI()

@app.get("/")
def root():
    return {"message":"Helloooooooooooooooo"}

@app.get("/posts")
def get_posts():
    return {"data":"These are yout posts"}

@app.post("/createpost")
def create_posts(data : dict = Body(...)):
    print(data)
    return {"message":"post created"}

