from fastapi import FastAPI
import json
app = FastAPI()

def load_data():
    with open("patients.json", "r") as f:
            data = json.load(f)
    return data


@app.get("/")
def base():
    return {"message": "Patient management system API is running!"}

@app.get("/about")
def about():
    return {"message": "This is a simple patient management system API."}

@app.get("/patients")
def get_patients():
    return load_data()



@app.get("/patients/{patient_id}")

def get_patient(patient_id: str):
    data = load_data()
    for patient in data:
        if patient_id==patient:
            return {"message": "Patient found", "patient": data[patient_id]}
    return {"error": "Patient not found"}   


