from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, computed_field
from typing import List, Literal, Annotated, Optional
from fastapi.responses import JSONResponse
import json
import logging
import os
from pathlib import Path as PathlibPath

# ========== Configure Logging ==========
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ========== Initialize FastAPI ==========
app = FastAPI(
    title="Patient Management System API",
    description="A comprehensive API for managing patient medical records",
    version="1.0.0"
)

# ========== Configure CORS ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

logger.info("Patient Management API initialized successfully")


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


# ========== Data File Management ==========
DATA_FILE_PATH = "data/patients.json"


def ensure_data_file_exists():
    """Ensure data directory and JSON file exist."""
    try:
        PathlibPath("data").mkdir(exist_ok=True)
        if not os.path.exists(DATA_FILE_PATH):
            with open(DATA_FILE_PATH, "w") as f:
                json.dump({}, f)
            logger.info(f"Created new data file at {DATA_FILE_PATH}")
    except Exception as e:
        logger.error(f"Error creating data file: {e}")
        raise


def load_data():
    """Load patient data from JSON file with error handling."""
    try:
        ensure_data_file_exists()
        with open(DATA_FILE_PATH, "r") as f:
            data = json.load(f)
            logger.debug(f"Successfully loaded {len(data)} patients from file")
            return data
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        raise HTTPException(status_code=500, detail="Data file is corrupted")
    except FileNotFoundError as e:
        logger.error(f"Data file not found: {e}")
        ensure_data_file_exists()
        return {}
    except Exception as e:
        logger.error(f"Unexpected error loading data: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to load patient data")


def save_data(data: dict):
    """Save patient data to JSON file with error handling."""
    try:
        ensure_data_file_exists()
        with open(DATA_FILE_PATH, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Successfully saved {len(data)} patients to file")
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to save patient data")


# ========== Information Endpoints ==========

@app.get("/", tags=["Info"])
def home() -> dict:
    """Welcome endpoint - Returns API greeting message."""
    logger.info("Home endpoint accessed")
    return {"message": "Patient Management System API"}


@app.get("/about", tags=["Info"])
def about() -> dict:
    """About endpoint - Returns information about the API."""
    logger.info("About endpoint accessed")
    return {"message": "A fully functional API to manage your patients records."}


@app.get("/services", tags=["Info"])
def services() -> dict:
    """Services endpoint - Returns available services."""
    logger.info("Services endpoint accessed")
    return {"message": "We provide our state of the art APIs for free"}


@app.get("/contact", tags=["Info"])
def contact() -> dict:
    """Contact endpoint - Returns contact information."""
    logger.info("Contact endpoint accessed")
    return {"message": "If any query please contact to +918605060204"}


# ========== Patient Data Retrieval Endpoints ==========

@app.get("/view", tags=["Patients"])
def view_data() -> dict:
    """Retrieve all patients - Returns complete patient database."""
    try:
        logger.info("Fetching all patients")
        data = load_data()
        logger.info(f"Successfully retrieved {len(data)} patients")
        return data
    except Exception as e:
        logger.error(f"Error retrieving all patients: {e}")
        raise


@app.get("/patient/{pat_id}", tags=["Patients"])
def search_patient(pat_id: str = Path(
    ...,
    description="Enter Patient ID",
    examples=["P001"]
)) -> dict:
    """Search patient by ID - Returns patient details if found."""
    try:
        logger.info(f"Searching for patient with ID: {pat_id}")
        data = load_data()

        if pat_id in data:
            logger.info(f"Patient {pat_id} found")
            return data[pat_id]

        logger.warning(f"Patient {pat_id} not found")
        raise HTTPException(
            status_code=404, detail=f"Patient with ID '{pat_id}' not found!")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching patient {pat_id}: {e}")
        raise HTTPException(status_code=500, detail="Error searching patient")


@app.get("/patient/name/{pat_name}", tags=["Patients"])
def search_name(pat_name: str = Path(
    ...,
    description="Enter the name of the patient",
    examples=["Ravi Mehta"]
)) -> dict:
    """Search patient by name - Returns first matching patient (case-insensitive)."""
    try:
        logger.info(f"Searching for patient with name: {pat_name}")
        data = load_data()

        for patient_id, patient_info in data.items():
            if patient_info["name"].lower() == pat_name.lower():
                logger.info(
                    f"Patient '{pat_name}' found with ID: {patient_id}")
                return patient_info

        logger.warning(f"Patient with name '{pat_name}' not found")
        raise HTTPException(
            status_code=404, detail=f"Patient '{pat_name}' not found!")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching patient by name '{pat_name}': {e}")
        raise HTTPException(status_code=500, detail="Error searching patient")


# ========== Sorting Endpoint ==========

@app.get("/sort", tags=["Patients"])
def sort_data(
    sort_by: str = Query(...,
                         description="Sort field: height, weight, or bmi"),
    order: str = Query(..., description="Sort order: asc or desc")
):
    """Sort patients by specified field and order."""
    try:
        valid_fields = ["height", "weight", "bmi"]
        valid_orders = ["asc", "desc"]

        if sort_by not in valid_fields:
            logger.warning(f"Invalid sort field: {sort_by}")
            raise HTTPException(
                status_code=400,
                detail=f"Invalid field! Choose from: {', '.join(valid_fields)}")

        if order not in valid_orders:
            logger.warning(f"Invalid sort order: {order}")
            raise HTTPException(
                status_code=400,
                detail=f"Invalid order! Choose from: {', '.join(valid_orders)}")

        logger.info(f"Sorting patients by {sort_by} in {order} order")
        data = load_data()

        if not data:
            logger.warning("No patients available to sort")
            return []

        sort_reverse = order == "desc"
        sorted_data = sorted(
            data.values(),
            key=lambda x: x.get(sort_by, 0),
            reverse=sort_reverse)

        logger.info(f"Successfully sorted {len(sorted_data)} patients")
        return sorted_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sorting patients: {e}")
        raise HTTPException(status_code=500, detail="Error sorting patients")


# ========== Patient Creation Endpoint ==========

@app.post("/new", tags=["Patients"], status_code=201)
def add_patient(patient: AddPatient):
    """Add a new patient - Creates a new patient record with auto-calculated BMI and verdict."""
    try:
        logger.info(f"Adding new patient with ID: {patient.id}")

        # Validate patient ID format
        if not patient.id.strip():
            logger.warning("Empty patient ID provided")
            raise HTTPException(
                status_code=400,
                detail="Patient ID cannot be empty")

        data = load_data()

        # Check if patient already exists
        if patient.id in data:
            logger.warning(f"Patient {patient.id} already exists")
            raise HTTPException(
                status_code=400,
                detail=f"Patient with ID '{patient.id}' already exists!")

        # Add patient to database
        data[patient.id] = patient.model_dump(exclude=['id'])
        save_data(data)

        logger.info(f"Successfully added patient {patient.id}: {patient.name}")
        return JSONResponse(
            status_code=201,
            content={"message": f"Patient {patient.id} added successfully!", "id": patient.id})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding patient: {e}")
        raise HTTPException(status_code=500, detail="Error adding patient")


# ========== Patient Update Endpoint ==========

@app.put("/update/{pat_id}", tags=["Patients"])
def update_patient(
        pat_id: str = Path(..., description="Patient ID to update"),
        pat_update: UpdatePatient = None):
    """Update patient information - Updates specified fields and recalculates BMI and verdict."""
    try:
        logger.info(f"Updating patient with ID: {pat_id}")
        data = load_data()

        if pat_id not in data:
            logger.warning(f"Patient {pat_id} not found for update")
            raise HTTPException(
                status_code=404,
                detail=f"Patient with ID '{pat_id}' not found!")

        # Get existing data
        existing_data = data[pat_id]

        # Update only provided fields
        updated_data = pat_update.model_dump(exclude_unset=True)
        for key, value in updated_data.items():
            existing_data[key] = value

        # Recalculate BMI and verdict
        existing_data['id'] = pat_id
        patient_pydantic_obj = AddPatient(**existing_data)
        data[pat_id] = patient_pydantic_obj.model_dump(exclude='id')

        save_data(data)

        logger.info(f"Successfully updated patient {pat_id}")
        return JSONResponse(
            status_code=200,
            content={"message": f"Patient {pat_id} updated successfully!"})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating patient {pat_id}: {e}")
        raise HTTPException(status_code=500, detail="Error updating patient")


# ========== Patient Deletion Endpoint ==========

@app.delete("/delete/{pat_id}", tags=["Patients"])
def delete_patient(pat_id: str = Path(..., description="Patient ID to delete")):
    """Delete a patient - Permanently removes patient record from the system."""
    try:
        logger.info(f"Deleting patient with ID: {pat_id}")
        data = load_data()

        if pat_id not in data:
            logger.warning(f"Patient {pat_id} not found for deletion")
            raise HTTPException(
                status_code=404,
                detail=f"Patient with ID '{pat_id}' not found!")

        patient_name = data[pat_id].get("name", "Unknown")
        del data[pat_id]
        save_data(data)

        logger.info(f"Successfully deleted patient {pat_id}: {patient_name}")
        return JSONResponse(
            status_code=200,
            content={"message": f"Patient {pat_id} ({patient_name}) deleted successfully!"})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting patient {pat_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting patient")
