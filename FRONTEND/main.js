// ========== API Configuration ==========
const API_BASE_URL = 'https://patient-management-app-rqjp.onrender.com';

// ========== State Management ==========
let allPatients = {};
let editingPatientId = null;
let deletePatientId = null;

// ========== Initialization ==========
document.addEventListener('DOMContentLoaded', () => {
    loadAllPatients();
    setupFormSubmit();
});

// ========== Setup Form Submit ==========
function setupFormSubmit() {
    const form = document.getElementById('patient-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await savePatient();
    });
}

// ========== Show Alert Messages ==========
function showAlert(message, type = 'success') {
    const alertContainer = document.getElementById('alert-container');
    const alertDiv = document.createElement('div');

    const bgColor = type === 'success' ? 'bg-green-100 border-green-500' : 'bg-red-100 border-red-500';
    const textColor = type === 'success' ? 'text-green-800' : 'text-red-800';

    alertDiv.className = `${bgColor} ${textColor} border-l-4 px-4 py-3 rounded mb-4 animate-pulse`;
    alertDiv.innerHTML = `
        <p class="font-bold">${type === 'success' ? '✅' : '❌'} ${message}</p>
    `;

    alertContainer.appendChild(alertDiv);

    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

// ========== Show Loading ==========
function showLoading(show = true) {
    const loadingIndicator = document.getElementById('loading-indicator');
    if (show) {
        loadingIndicator.classList.remove('hidden');
    } else {
        loadingIndicator.classList.add('hidden');
    }
}

// ========== CRUD Operations ==========

// Load All Patients
async function loadAllPatients() {
    showLoading(true);
    try {
        const response = await fetch(`${API_BASE_URL}/view`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        allPatients = await response.json();
        displayPatients(allPatients);
        updatePatientCount();
        showAlert('Patients loaded successfully!', 'success');
    } catch (error) {
        console.error('Error loading patients:', error);
        showAlert('Failed to load patients. Check your internet connection.', 'error');
        displayPatients({});
    } finally {
        showLoading(false);
    }
}

// Display Patients as Cards
function displayPatients(patients) {
    const container = document.getElementById('patients-container');

    if (!patients || Object.keys(patients).length === 0) {
        container.innerHTML = `
            <div class="col-span-full text-center py-12 text-gray-500">
                <p class="text-lg">📋 No patients found. Click "Add Patient" to get started!</p>
            </div>
        `;
        return;
    }

    container.innerHTML = '';

    Object.entries(patients).forEach(([patientId, patient]) => {
        const bmiStatus = getBMIStatus(patient.bmi);
        const card = document.createElement('div');
        card.className = 'bg-white rounded-lg shadow-md hover:shadow-lg transition-all p-4 sm:p-6';

        card.innerHTML = `
            <div class="flex justify-between items-start mb-4">
                <div>
                    <h3 class="text-lg sm:text-xl font-bold text-gray-800">${patient.name}</h3>
                    <p class="text-gray-500 text-sm">ID: ${patientId}</p>
                </div>
                <span class="bg-indigo-100 text-indigo-800 text-xs sm:text-sm px-3 py-1 rounded-full font-semibold">${bmiStatus}</span>
            </div>
            
            <div class="grid grid-cols-2 gap-3 mb-4 text-sm">
                <div class="bg-blue-50 p-3 rounded-lg">
                    <p class="text-gray-600 text-xs">Age</p>
                    <p class="font-bold text-lg">${patient.age}</p>
                </div>
                <div class="bg-green-50 p-3 rounded-lg">
                    <p class="text-gray-600 text-xs">City</p>
                    <p class="font-bold">${patient.city}</p>
                </div>
                <div class="bg-purple-50 p-3 rounded-lg">
                    <p class="text-gray-600 text-xs">BMI</p>
                    <p class="font-bold">${patient.bmi}</p>
                </div>
                <div class="bg-yellow-50 p-3 rounded-lg">
                    <p class="text-gray-600 text-xs">Weight</p>
                    <p class="font-bold">${patient.weight}kg</p>
                </div>
            </div>
            
            <p class="text-gray-700 mb-4 text-sm">
                <strong>Status:</strong> <span class="${getBMIStatusColor(patient.bmi)}">${patient.verdict}</span>
            </p>
            
            <div class="flex gap-2">
                <button onclick="viewPatientDetails('${patientId}')" class="flex-1 bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-3 rounded transition-all text-sm">
                    👁️ View
                </button>
                <button onclick="editPatient('${patientId}')" class="flex-1 bg-orange-500 hover:bg-orange-600 text-white font-bold py-2 px-3 rounded transition-all text-sm">
                    ✏️ Edit
                </button>
                <button onclick="initiateDelete('${patientId}')" class="flex-1 bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-3 rounded transition-all text-sm">
                    🗑️ Delete
                </button>
            </div>
        `;

        container.appendChild(card);
    });
}

// Get BMI Status Color
function getBMIStatusColor(bmi) {
    if (bmi < 18.5) return 'text-orange-600 font-semibold';
    if (bmi < 24.9) return 'text-green-600 font-semibold';
    if (bmi < 30) return 'text-yellow-600 font-semibold';
    if (bmi < 35) return 'text-red-600 font-semibold';
    return 'text-red-700 font-semibold';
}

// Get BMI Status Badge
function getBMIStatus(bmi) {
    if (bmi < 18.5) return '🟠 Underweight';
    if (bmi < 24.9) return '🟢 Normal';
    if (bmi < 30) return '🟡 Overweight';
    if (bmi < 35) return '🔴 Obese';
    return '🔴 Extremely Obese';
}

// Update Patient Count
function updatePatientCount() {
    document.getElementById('patient-count').textContent = Object.keys(allPatients).length;
}

// ========== Modal Functions ==========

// Add Patient Modal
function toggleAddPatientModal() {
    const modal = document.getElementById('add-patient-modal');
    modal.classList.toggle('hidden');

    if (modal.classList.contains('hidden')) {
        clearPatientForm();
        editingPatientId = null;
    }
}

// Search Modal
function toggleSearchModal() {
    const modal = document.getElementById('search-modal');
    modal.classList.toggle('hidden');

    if (modal.classList.contains('hidden')) {
        document.getElementById('search-results').classList.add('hidden');
        document.getElementById('search-id-input').value = '';
        document.getElementById('search-name-input').value = '';
    }
}

// Detail Modal
function closeDetailModal() {
    document.getElementById('detail-modal').classList.add('hidden');
}

// Sort Modal
function openSortModal() {
    document.getElementById('sort-modal').classList.remove('hidden');
}

function closeSortModal() {
    document.getElementById('sort-modal').classList.add('hidden');
}

// Delete Modal
function closeDeleteModal() {
    document.getElementById('delete-modal').classList.add('hidden');
    deletePatientId = null;
}

// ========== Patient Operations ==========

// Clear Form
function clearPatientForm() {
    document.getElementById('patient-form').reset();
    document.getElementById('patient-id').disabled = false;
    document.getElementById('modal-title').textContent = 'Add New Patient';
    document.getElementById('submit-btn').textContent = 'Save Patient';
}

// Save Patient (Add/Update)
async function savePatient() {
    const patientId = document.getElementById('patient-id').value;
    const name = document.getElementById('patient-name').value;
    const age = parseInt(document.getElementById('patient-age').value);
    const city = document.getElementById('patient-city').value;
    const gender = document.getElementById('patient-gender').value;
    const height = parseFloat(document.getElementById('patient-height').value);
    const weight = parseFloat(document.getElementById('patient-weight').value);

    // Validation
    if (!patientId || !name || !age || !city || !gender || !height || !weight) {
        showAlert('Please fill in all required fields!', 'error');
        return;
    }

    if (age < 1 || age > 119) {
        showAlert('Age must be between 1 and 119!', 'error');
        return;
    }

    showLoading(true);

    try {
        if (editingPatientId) {
            // Update Patient
            const response = await fetch(`${API_BASE_URL}/update/${editingPatientId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name,
                    age,
                    city,
                    gender,
                    height,
                    weight
                })
            });

            if (!response.ok) {
                throw new Error('Failed to update patient');
            }

            showAlert('✅ Patient updated successfully!', 'success');
            editingPatientId = null;
        } else {
            // Add New Patient
            const response = await fetch(`${API_BASE_URL}/new`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    id: patientId,
                    name,
                    age,
                    city,
                    gender,
                    height,
                    weight
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to add patient');
            }

            showAlert('✅ Patient added successfully!', 'success');
        }

        clearPatientForm();
        toggleAddPatientModal();
        loadAllPatients();
    } catch (error) {
        console.error('Error saving patient:', error);
        showAlert(`Error: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

// Edit Patient
function editPatient(patientId) {
    const patient = allPatients[patientId];

    editingPatientId = patientId;
    document.getElementById('patient-id').value = patientId;
    document.getElementById('patient-id').disabled = true;
    document.getElementById('patient-name').value = patient.name;
    document.getElementById('patient-age').value = patient.age;
    document.getElementById('patient-city').value = patient.city;
    document.getElementById('patient-gender').value = patient.gender;
    document.getElementById('patient-height').value = patient.height;
    document.getElementById('patient-weight').value = patient.weight;

    document.getElementById('modal-title').textContent = `Edit Patient - ${patientId}`;
    document.getElementById('submit-btn').textContent = 'Update Patient';

    document.getElementById('add-patient-modal').classList.remove('hidden');
}

// View Patient Details
function viewPatientDetails(patientId) {
    const patient = allPatients[patientId];
    const detailContent = document.getElementById('detail-content');

    detailContent.innerHTML = `
        <div class="space-y-4">
            <div class="bg-gray-50 p-4 rounded-lg">
                <p class="text-gray-600 text-sm">Patient ID</p>
                <p class="font-bold text-lg">${patientId}</p>
            </div>
            
            <div class="grid grid-cols-2 gap-4">
                <div class="bg-blue-50 p-4 rounded-lg">
                    <p class="text-gray-600 text-sm">Name</p>
                    <p class="font-bold">${patient.name}</p>
                </div>
                <div class="bg-green-50 p-4 rounded-lg">
                    <p class="text-gray-600 text-sm">Age</p>
                    <p class="font-bold text-lg">${patient.age}</p>
                </div>
            </div>
            
            <div class="grid grid-cols-2 gap-4">
                <div class="bg-purple-50 p-4 rounded-lg">
                    <p class="text-gray-600 text-sm">City</p>
                    <p class="font-bold">${patient.city}</p>
                </div>
                <div class="bg-yellow-50 p-4 rounded-lg">
                    <p class="text-gray-600 text-sm">Gender</p>
                    <p class="font-bold capitalize">${patient.gender}</p>
                </div>
            </div>
            
            <div class="grid grid-cols-2 gap-4">
                <div class="bg-orange-50 p-4 rounded-lg">
                    <p class="text-gray-600 text-sm">Height</p>
                    <p class="font-bold">${patient.height} m</p>
                </div>
                <div class="bg-red-50 p-4 rounded-lg">
                    <p class="text-gray-600 text-sm">Weight</p>
                    <p class="font-bold">${patient.weight} kg</p>
                </div>
            </div>
            
            <div class="bg-indigo-50 p-4 rounded-lg border-2 border-indigo-200">
                <p class="text-gray-600 text-sm">BMI</p>
                <p class="font-bold text-2xl text-indigo-600">${patient.bmi}</p>
            </div>
            
            <div class="bg-gradient-to-r from-green-100 to-blue-100 p-4 rounded-lg border-2 border-green-300">
                <p class="text-gray-600 text-sm">Health Status</p>
                <p class="font-bold text-lg ${getBMIStatusColor(patient.bmi)}">${patient.verdict}</p>
            </div>
        </div>
    `;

    document.getElementById('detail-modal').classList.remove('hidden');
}

// Initiate Delete
function initiateDelete(patientId) {
    deletePatientId = patientId;
    document.getElementById('delete-patient-name').textContent = allPatients[patientId].name;
    document.getElementById('delete-modal').classList.remove('hidden');
}

// Confirm Delete
async function confirmDelete() {
    if (!deletePatientId) return;

    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/delete/${deletePatientId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error('Failed to delete patient');
        }

        showAlert('✅ Patient deleted successfully!', 'success');
        closeDeleteModal();
        loadAllPatients();
    } catch (error) {
        console.error('Error deleting patient:', error);
        showAlert('Failed to delete patient', 'error');
    } finally {
        showLoading(false);
    }
}

// ========== Search Operations ==========

// Search Patient by ID
async function searchPatientById() {
    const patientId = document.getElementById('search-id-input').value.trim();

    if (!patientId) {
        showAlert('Please enter a Patient ID', 'error');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/patient/${patientId}`);

        if (!response.ok) {
            throw new Error('Patient not found');
        }

        const patient = await response.json();
        displaySearchResults({ [patientId]: patient });
    } catch (error) {
        console.error('Error searching patient:', error);
        showAlert('Patient not found', 'error');
        document.getElementById('search-results').classList.add('hidden');
    } finally {
        showLoading(false);
    }
}

// Search Patient by Name
async function searchPatientByName() {
    const patientName = document.getElementById('search-name-input').value.trim();

    if (!patientName) {
        showAlert('Please enter a Patient Name', 'error');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/patient/name/${encodeURIComponent(patientName)}`);

        if (!response.ok) {
            throw new Error('Patient not found');
        }

        // Find the patient ID by searching through allPatients
        let foundPatientId = null;
        for (const [id, patient] of Object.entries(allPatients)) {
            if (patient.name.toLowerCase() === patientName.toLowerCase()) {
                foundPatientId = id;
                break;
            }
        }

        const patient = await response.json();
        displaySearchResults(foundPatientId ? { [foundPatientId]: patient } : { 'Unknown': patient });
    } catch (error) {
        console.error('Error searching patient by name:', error);
        showAlert('Patient not found', 'error');
        document.getElementById('search-results').classList.add('hidden');
    } finally {
        showLoading(false);
    }
}

// Display Search Results
function displaySearchResults(results) {
    const searchResults = document.getElementById('search-results');
    searchResults.classList.remove('hidden');

    if (!results || Object.keys(results).length === 0) {
        searchResults.innerHTML = '<p class="text-gray-500">No patients found</p>';
        return;
    }

    let html = '';
    Object.entries(results).forEach(([patientId, patient]) => {
        html += `
            <div class="bg-white p-4 rounded-lg border-2 border-blue-200 mb-3">
                <div class="flex justify-between items-start mb-2">
                    <div>
                        <h4 class="font-bold text-gray-800">${patient.name}</h4>
                        <p class="text-gray-500 text-sm">ID: ${patientId}</p>
                    </div>
                    <span class="text-sm font-semibold ${getBMIStatusColor(patient.bmi)}">${patient.verdict}</span>
                </div>
                <p class="text-gray-600 text-sm">Age: ${patient.age} | City: ${patient.city} | BMI: ${patient.bmi}</p>
                <div class="mt-3 flex gap-2">
                    <button onclick="viewPatientDetails('${patientId}'); toggleSearchModal()" class="flex-1 bg-blue-500 hover:bg-blue-600 text-white font-bold py-1 px-2 rounded text-sm">
                        View
                    </button>
                    <button onclick="editPatient('${patientId}'); toggleSearchModal()" class="flex-1 bg-orange-500 hover:bg-orange-600 text-white font-bold py-1 px-2 rounded text-sm">
                        Edit
                    </button>
                </div>
            </div>
        `;
    });

    searchResults.innerHTML = html;
}

// ========== Sort Operations ==========

// Sort Patients
async function sortPatients() {
    const sortBy = document.getElementById('sort-by').value;
    const sortOrder = document.getElementById('sort-order').value;

    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/sort?sort_by=${sortBy}&order=${sortOrder}`);

        if (!response.ok) {
            throw new Error('Failed to sort patients');
        }

        const sortedPatients = await response.json();

        // Convert array back to object format with IDs
        let sortedPatientsDict = {};
        sortedPatients.forEach((patient, index) => {
            sortedPatientsDict[`Patient ${index + 1}`] = patient;
        });

        displayPatients(sortedPatients);
        showAlert(`✅ Sorted by ${sortBy} (${sortOrder})`, 'success');
        closeSortModal();
    } catch (error) {
        console.error('Error sorting patients:', error);
        showAlert('Failed to sort patients', 'error');
    } finally {
        showLoading(false);
    }
}
