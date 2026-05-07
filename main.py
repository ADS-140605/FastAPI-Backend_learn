from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def base():
    return {"message": "Hello World"}

@app.get("/hello")
async def hello(name: str):
    return {"message": f"Hello {name}!"}
