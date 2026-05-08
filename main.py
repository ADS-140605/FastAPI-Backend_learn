from fastapi import FastAPI, HTTPException, Path
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
def get_patient(patient_id: str =Path(..., description="The ID of the patient to retrieve", example="P001")):
    data = load_data()
    for patient in data:
        if patient_id==patient:
            return {"message": "Patient found", "patient": data[patient_id]}
    raise HTTPException (status_code=404, detail="Patient not found")


