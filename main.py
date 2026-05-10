from fastapi import FastAPI, HTTPException, Path ,Query
from fastapi.responses import JSONResponse
from typing import Annotated, Literal, Optional
import json
from pydantic import BaseModel
from pydantic import Field,computed_field




class Patient(BaseModel):
    id: Annotated[str, Field(..., description="The ID of the patient", example="P001")]
    name: Annotated[str, Field(..., description="The name of the patient", example="John Doe")]
    age: Annotated[int, Field(...,gt=0,lt=150, description="The age of the patient", example=30)]
    height: Annotated[float, Field(...,gt=0, description="The height of the patient", example=175.5)]
    weight: Annotated[float, Field(...,gt=0, description="The weight of the patient", example=70.0)]
    gender: Annotated[Literal["Male", "Female","Other"], Field(..., description="The gender of the patient", example="Male")]
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / ((self.height / 100) ** 2)
    @computed_field
    @property
    def verdict(self)-> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 25:
            return "Normal weight"
        elif 25 <= self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"
        


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(None, description="The name of the patient", example="John Doe")]
    age: Annotated[Optional[int], Field(None,gt=0,lt=150, description="The age of the patient", example=30)]
    height: Annotated[Optional[float], Field(None,gt=0, description="The height of the patient", example=175.5)]
    weight: Annotated[Optional[float], Field(None,gt=0, description="The weight of the patient", example=70.0)]   
    gender: Annotated[Optional[Literal["Male", "Female","Other"]], Field(None, description="The gender of the patient", example="Male")]       


app = FastAPI()

def load_data():
    with open("patients.json", "r") as f:
            data = json.load(f)
    return data


def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)



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




@app.post("/new_patient")
def add_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists.")
    data[patient.id] = patient.model_dump(exclude={'id'})
    save_data(data)
    return JSONResponse(status_code=201, content={"message": "Patient added successfully", "patient": patient.dict()})




@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: str = Path(..., description="The ID of the patient to delete", example="P001")):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    del data[patient_id]
    save_data(data)
    return {"message": "Patient deleted successfully"}



@app.put("/update_patient/{patient_id}")
def update_patient(
    patient_update: PatientUpdate,
    patient_id: str = Path(
        ...,
        description="The ID of the patient to update"
    )
):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    existing_patient = data[patient_id]

    updated_patient = patient_update.model_dump(
        exclude_unset=True,
        exclude={"id"}
    )

    for key, value in updated_patient.items():
        existing_patient[key] = value

    existing_patient["id"] = patient_id

    validated_patient = Patient(**existing_patient)

    data[patient_id] = validated_patient.model_dump(
        exclude={"id"}
    )

    save_data(data)

    return JSONResponse(
        status_code=200,
        content={
            "message": "Patient updated successfully",
            "patient": validated_patient.model_dump()
        }
    )