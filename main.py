from fastapi import FastAPI
import json
app = FastAPI()

def load_data():
    with open("patients.json", "r") as f:
            data = json.load(f)
    return {"patients": list(data.values())}


@app.get("/")
def base():
    return {"message": "Patient management system API is running!"}

@app.get("/about")
def about():
    return {"message": "This is a simple patient management system API."}

@app.get("/patients")
def get_patients():
    return load_data()


