from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field, computed_field
from typing import List, Literal, Annotated, Optional
from fastapi.responses import JSONResponse
import json

app = FastAPI()


# schema for adding patients
class AddPatient(BaseModel):
    id: Annotated[str, Field(..., description="Enter Patient ID", examples=[
                             'P001', 'P002'])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    age: Annotated[int, Field(..., gt=0, lt=120,
                              description="Age of the patient")]
    city: Annotated[str,
                    Field(..., description="City of residence of the patient")]
    gender: Annotated[Literal["male", "female", "other"],
                      Field(..., description="Gender of the patient")]
    height: Annotated[float,
                      Field(..., description="Height of the patient in m")]
    weight: Annotated[float,
                      Field(..., description="Weight of the patient in kg")]

    # computing bmi
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height**2), 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 24.9:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        elif self.bmi < 35:
            return "Obese"
        else:
            return "Extremely Obese"


# schema for updating patients
class UpdatePatient(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120)]
    city: Annotated[Optional[str], Field(default=None)]
    gender: Annotated[Optional[Literal["male",
                                       "female", "other"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


# helper function to load json file

def load_data():
    with open("data/patients.json") as f:
        data = json.load(f)
        return data


def save_data(data):
    with open("data/patients.json", "w") as f:
        json.dump(data, f)


@app.get("/")
def home() -> dict:
    return {"message": "Patient Management System API"}


@app.get("/about")
def about() -> dict:
    return {"message": "A fully functional API to manage your patients records."}


@app.get("/services")
def services() -> dict:
    return {"message": "We provide our state of the art APIs for free"}


@app.get("/contact")
def contact() -> dict:
    return {"message": "If any query please contact to +918605060204"}


@app.get("/view")
def view_data() -> dict:
    data = load_data()
    return data


# Implemeting Path parameter
# search patient by ID
@app.get("/patient/{pat_id}")
def search_patient(pat_id: str = Path(
    ...,
    description="Enter Patient ID",
    examples=["P001"]
)) -> dict:
    data = load_data()

    if pat_id in data:
        return data[pat_id]

    raise HTTPException(status_code=404, detail="Patient Not Found!")


# search patient by name
@app.get("/patient/name/{pat_name}")
def search_name(pat_name: str = Path(
    ...,
    description="Enter the name of the patient",
    examples=["Ravi Mehta"]
)) -> dict:
    data = load_data()

    for patient_id, patient_info in data.items():
        if patient_info["name"].lower() == pat_name.lower():
            return patient_info

    raise HTTPException(
        status_code=404, detail=f"Patient '{pat_name}' Not Found!")


# Implemeting Query parameter
# sort patient by weight, height and BMI or in ascending or descending order
@app.get("/sort")
def sort_data(
    sort_by: str = Query(...,
                         description="Sort on the basis of height, weight and BMI"),
    order: str = Query(description="sort in ascending or descending order")
):
    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=404, detail=f"Invalid Filed! select from {valid_fields}")

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=404, detail="Invalid Order! select between asc or desc")

    data = load_data()

    if order == "asc":
        sort_order = False
    else:
        sort_order = True

    sorted_data = sorted(
        data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data


# create new patient records

@app.post("/new")
def add_patient(patient: AddPatient):
    data = load_data()

    # check if patient already exists
    if patient.id in data:
        raise HTTPException(
            status_code=400, detail=f"Patient with ID '{patient.id}' already exists!")

    # converting a pydantic obj into dict
    data[patient.id] = patient.model_dump(exclude=['id'])

    # saving the new data into json file
    save_data(data)

    return JSONResponse(status_code=201, content={"message": "Patient Added Successfully!"})


# TODO: add ai for bmi and verdict prediction


# update route
@app.put("/update/{pat_id}")
def update_patient(pat_id: str, pat_update: UpdatePatient):
    data = load_data()

    if pat_id not in data:
        raise HTTPException(status_code=404, detail="Patient ID Not Found!")

    # existing data
    existing_data = data[pat_id]

    # converting pydantic model to dict
    updated_data = pat_update.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        existing_data[key] = value

    # convert existing_data to pydantic object then it will update bmi & verdict
    existing_data['id'] = pat_id
    patient_pydantic_obj = AddPatient(**existing_data)

    # pydantic obj -> dict
    existing_data = patient_pydantic_obj.model_dump(exclude='id')

    # add this to dict
    data[pat_id] = existing_data

    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient UPDATED Successfully!"})


# delete route
@app.delete("/delete/{pat_id}")
def delete_patient(pat_id: str):
    data = load_data()

    if pat_id not in data:
        raise HTTPException(status_code=404, detail="Patient ID Not Found!")

    del data[pat_id]

    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient DELETED Successfully!"})
