from fastapi import FastAPI, HTTPException, Path ,Query
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
    data= load_data()
    return {"message": "List of patients", "patients": data}



@app.get("/patients/{patient_id}")
def get_patient(patient_id: str =Path(..., description="The ID of the patient to retrieve", example="P001")):
    data = load_data()
    for patient in data:
        if patient_id==patient:
            return {"message": "Patient found", "patient": data[patient_id]}
    raise HTTPException (status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="The field to sort patients by('bmi', 'age' ,'height')", example="age"),order:str = Query("asc", description="The order to sort patients by('asc' for ascending, 'desc' for descending)", example="asc")):
    data = load_data()
    if sort_by not in ['bmi', 'age', 'height']:
        raise HTTPException(status_code=400, detail="Invalid sort field. Must be 'bmi', 'age', or 'height'.")
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid sort order. Must be 'asc' or 'desc'.")
    
    sorted_patients = sorted(data.items(), key=lambda x: x[1][sort_by], reverse=(order == "desc"))
    return {"message": f"Patients sorted by {sort_by} in {order} order", "patients": dict(sorted_patients)}