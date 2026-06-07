from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Helloooooooooooooooo"}

@app.get("/posts")
async def get_posts():
    return {"data":"These are yout posts"}

