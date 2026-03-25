# Patient Management API 🏥

A comprehensive FastAPI-based REST API for managing patient medical records. This application provides full CRUD operations for patient data with automatic health metrics calculation and intelligent sorting capabilities.

## 📋 Requirements

- Python 3.8+
- FastAPI
- Pydantic
- Uvicorn

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd patient_management_app
```

### 2. Create Virtual Environment

```bash
# On Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
uvicorn app:app --reload
```

The API will be available at: `http://localhost:8000`

### 5. Access Documentation

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>

## 📡 API Endpoints

### Information Endpoints

#### 1. Home

```
GET /
```

Returns a welcome message.

**Response:**

```json
{
  "message": "Patient Management System API"
}
```

#### 2. About

```
GET /about
```

Returns information about the API.

**Response:**

```json
{
  "message": "A fully functional API to manage your patients records."
}
```

#### 3. Services

```
GET /services
```

Returns available services information.

**Response:**

```json
{
  "message": "We provide our state of the art APIs for free"
}
```

#### 4. Contact

```
GET /contact
```

Returns contact information.

**Response:**

```json
{
  "message": "If any query please contact to +918605060204"
}
```

---

### Patient Data Endpoints

#### 5. View All Patients

```
GET /view
```

Retrieves all patient records.

**Response:**

```json
{
  "P001": {
    "name": "John Doe",
    "age": 30,
    "city": "New York",
    "gender": "male",
    "height": 1.75,
    "weight": 75,
    "bmi": 24.49,
    "verdict": "Normal"
  },
  "P002": {
    "name": "Jane Smith",
    "age": 28,
    "city": "Los Angeles",
    "gender": "female",
    "height": 1.65,
    "weight": 62,
    "bmi": 22.77,
    "verdict": "Normal"
  }
}
```

#### 6. Search Patient by ID

```
GET /patient/{pat_id}
```

Retrieves a specific patient by their ID.

**Parameters:**

- `pat_id` (path parameter): Patient ID (e.g., "P001")

**Example:**

```
GET /patient/P001
```

**Response:**

```json
{
  "name": "John Doe",
  "age": 30,
  "city": "New York",
  "gender": "male",
  "height": 1.75,
  "weight": 75,
  "bmi": 24.49,
  "verdict": "Normal"
}
```

**Error Response (404):**

```json
{
  "detail": "Patient Not Found!"
}
```

#### 7. Search Patient by Name

```
GET /patient/name/{pat_name}
```

Retrieves a patient by their name (case-insensitive).

**Parameters:**

- `pat_name` (path parameter): Patient's full name (e.g., "John Doe")

**Example:**

```
GET /patient/name/John%20Doe
```

**Response:**

```json
{
  "name": "John Doe",
  "age": 30,
  "city": "New York",
  "gender": "male",
  "height": 1.75,
  "weight": 75,
  "bmi": 24.49,
  "verdict": "Normal"
}
```

#### 8. Sort Patients

```
GET /sort
```

Sorts all patients by a specific metric.

**Query Parameters:**

- `sort_by` (required): Field to sort by - `height`, `weight`, or `bmi`
- `order` (required): Sort order - `asc` (ascending) or `desc` (descending)

**Example:**

```
GET /sort?sort_by=bmi&order=desc
```

**Response:**

```json
[
  {
    "name": "Patient with Highest BMI",
    "age": 45,
    "city": "Texas",
    "gender": "male",
    "height": 1.70,
    "weight": 95,
    "bmi": 32.87,
    "verdict": "Extremely Obese"
  },
  {
    "name": "Patient with Lower BMI",
    "age": 28,
    "city": "California",
    "gender": "female",
    "height": 1.68,
    "weight": 58,
    "bmi": 20.54,
    "verdict": "Normal"
  }
]
```

---

### Patient Creation Endpoint

#### 9. Add New Patient

```
POST /new
```

Creates a new patient record.

**Request Body:**

```json
{
  "id": "P003",
  "name": "Alice Johnson",
  "age": 35,
  "city": "Chicago",
  "gender": "female",
  "height": 1.68,
  "weight": 65
}
```

**Parameters:**

- `id`: Unique patient identifier (e.g., "P001", "P002")
- `name`: Patient's full name
- `age`: Age (must be between 1 and 119)
- `city`: City of residence
- `gender`: One of `male`, `female`, or `other`
- `height`: Height in meters (float)
- `weight`: Weight in kilograms (float)

**Success Response (201):**

```json
{
  "message": "Patient Added Successfully!"
}
```

**Error Response (400):**

```json
{
  "detail": "Patient with ID 'P003' already exists!"
}
```

---

### Patient Update Endpoint

#### 10. Update Patient

```
PUT /update/{pat_id}
```

Updates an existing patient's information. All fields are optional.

**Parameters:**

- `pat_id` (path parameter): Patient ID to update

**Request Body (all fields optional):**

```json
{
  "age": 36,
  "weight": 68,
  "city": "Boston"
}
```

**Fields:**

- `name`: Patient's name (optional)
- `age`: Age (optional, must be 1-119)
- `city`: City (optional)
- `gender`: Gender (optional)
- `height`: Height in meters (optional)
- `weight`: Weight in kilograms (optional)

**Success Response (200):**

```json
{
  "message": "Patient UPDATED Successfully!"
}
```

**Note:** BMI and health verdict are automatically recalculated after update.

---

### Patient Deletion Endpoint

#### 11. Delete Patient

```
DELETE /delete/{pat_id}
```

Removes a patient record from the system.

**Parameters:**

- `pat_id` (path parameter): Patient ID to delete

**Example:**

```
DELETE /delete/P003
```

**Success Response (200):**

```json
{
  "message": "Patient DELETED Successfully!"
}
```

**Error Response (404):**

```json
{
  "detail": "Patient ID Not Found!"
}
```

---

## 📊 Data Schema

### AddPatient Model

Used for creating new patients. Includes computed fields for BMI and health verdict.

```python
{
  "id": "string",           # Unique patient identifier
  "name": "string",         # Patient's full name
  "age": integer,           # Age (0 < age < 120)
  "city": "string",         # City of residence
  "gender": "string",       # "male", "female", or "other"
  "height": float,          # Height in meters
  "weight": float,          # Weight in kilograms
  "bmi": float,             # Computed: weight / (height²)
  "verdict": "string"       # Computed: Health status based on BMI
}
```

### BMI Categories & Verdicts

| BMI Range | Verdict |
|-----------|---------|
| < 18.5 | Underweight |
| 18.5 - 24.9 | Normal |
| 25 - 29.9 | Overweight |
| 30 - 34.9 | Obese |
| ≥ 35 | Extremely Obese |

### UpdatePatient Model

Used for updating existing patients. All fields are optional.

```python
{
  "name": "string (optional)",
  "age": integer (optional),
  "city": "string (optional)",
  "gender": "string (optional)",
  "height": float (optional),
  "weight": float (optional)
}
```

---

## 📁 Project Structure

```
patient_management_app/
├── app.py                 # Main FastAPI application
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── pyproject.toml         # Project configuration
├── data/
│   └── patients.json      # Patient records storage
├── .venv/                 # Virtual environment (ignored in git)
└── __pycache__/          # Python cache (ignored in git)
```

---

## 🔧 Example Usage

### Using cURL

**1. Add a new patient:**

```bash
curl -X POST "http://localhost:8000/new" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "P001",
    "name": "John Doe",
    "age": 30,
    "city": "New York",
    "gender": "male",
    "height": 1.75,
    "weight": 75
  }'
```

**2. Search patient by ID:**

```bash
curl -X GET "http://localhost:8000/patient/P001"
```

**3. Sort by BMI (descending):**

```bash
curl -X GET "http://localhost:8000/sort?sort_by=bmi&order=desc"
```

**4. Update patient:**

```bash
curl -X PUT "http://localhost:8000/update/P001" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 31,
    "weight": 77
  }'
```

**5. Delete patient:**

```bash
curl -X DELETE "http://localhost:8000/delete/P001"
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Add patient
response = requests.post(f"{BASE_URL}/new", json={
    "id": "P001",
    "name": "John Doe",
    "age": 30,
    "city": "New York",
    "gender": "male",
    "height": 1.75,
    "weight": 75
})
print(response.json())

# Get all patients
response = requests.get(f"{BASE_URL}/view")
print(response.json())

# Search by ID
response = requests.get(f"{BASE_URL}/patient/P001")
print(response.json())
```

---

## 📝 Data Storage

Patient records are stored in `data/patients.json` in the following format:

```json
{
  "P001": {
    "name": "John Doe",
    "age": 30,
    "city": "New York",
    "gender": "male",
    "height": 1.75,
    "weight": 75,
    "bmi": 24.49,
    "verdict": "Normal"
  },
  "P002": {
    "name": "Jane Smith",
    "age": 28,
    "city": "Los Angeles",
    "gender": "female",
    "height": 1.65,
    "weight": 62,
    "bmi": 22.77,
    "verdict": "Normal"
  }
}
```

---

## ⚙️ Configuration

### Environment Variables (Optional)

You can extend the application to support environment variables:

```bash
# .env file
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true
```

### Running on Different Host/Port

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Use a different port
uvicorn app:app --port 8001
```

### Module Not Found

```bash
# Ensure virtual environment is activated
.\.venv\Scripts\Activate.ps1
```

### JSON File Not Found

Create the `data` directory and `patients.json` file:

```bash
mkdir data
echo "{}" > data/patients.json
```

---

## 👨‍💻 Author

Developed with ❤️ for healthcare management.

---

**Last Updated:** March 2026
**API Version:** 1.0.0
