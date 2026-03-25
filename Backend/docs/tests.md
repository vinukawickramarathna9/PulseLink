# Postman API Testing Guide

This document contains testing instructions and payloads for testing the Clinical Appointment Scheduling System backend APIs using Postman.

## Setup Instructions

1. **Create a Postman Environment**:
   - Create a new environment named `Clinical Scheduler API - Local`.
   - Add a variable `base_url` and set its initial & current value to `http://localhost:5000`.
   - Add a variable `token` (leave value blank, this will be updated after login).

2. **Authorization Headers**:
   - For all endpoints (except Registration, Login, and specific public ones like Doctor Search), you must include the Authorization header.
   - Go to the **Authorization** tab -> Select **Bearer Token** -> Set the Token field to `{{token}}`.

---

## 1. Authentication & User Management

### 1.1 Register New User
* **Method & URL**: `POST {{base_url}}/api/auth/register`
* **Headers**: `Content-Type: application/json`
* **Body (raw JSON)**:
  ```json
  {
    "email": "user@example.com",
    "password": "Password123!",
    "firstName": "John",
    "lastName": "Doe",
    "role": "patient",
    "phone": "+1234567890"
  }
  ```
* **Expected Response**: `201 Created`

### 1.2 User Login
* **Method & URL**: `POST {{base_url}}/api/auth/login`
* **Headers**: `Content-Type: application/json`
* **Body (raw JSON)**:
  ```json
  {
    "email": "user@example.com",
    "password": "Password123!"
  }
  ```
* **Expected Response**: `200 OK`. 
  * *Note: Copy the `token` from the response and paste it into your `token` environment variable.*

### 1.3 Refresh Token
* **Method & URL**: `POST {{base_url}}/api/auth/refresh-token`
* **Headers**: `Content-Type: application/json`
* **Body (raw JSON)**:
  ```json
  {
    "refreshToken": "your_refresh_token_here"
  }
  ```
* **Expected Response**: `200 OK` (Returns the new token)

### 1.4 Get Profile
* **Method & URL**: `GET {{base_url}}/api/auth/profile`
* **Headers**: `Authorization: Bearer {{token}}`
* **Expected Response**: `200 OK`

---

## 2. Patient Management (Requires Patient Token)

### 2.1 Get Patient Dashboard
* **Method & URL**: `GET {{base_url}}/api/patients/dashboard`
* **Headers**: `Authorization: Bearer {{token}}`
* **Expected Response**: `200 OK`

### 2.2 Add Health Metric
* **Method & URL**: `POST {{base_url}}/api/patients/health-metrics`
* **Headers**: `Authorization: Bearer {{token}}`, `Content-Type: application/json`
* **Body (raw JSON)**:
  ```json
  {
    "bloodPressure": "120/80",
    "heartRate": 72,
    "weight": 70.5,
    "height": 175,
    "date": "2024-03-20"
  }
  ```
* **Expected Response**: `201 Created`

### 2.3 Search Doctors (Public endpoint)
* **Method & URL**: `GET {{base_url}}/api/doctors/search?specialty=cardiology`
* **Headers**: None required
* **Expected Response**: `200 OK`

### 2.4 Book Queue Appointment
* **Method & URL**: `POST {{base_url}}/api/patients/appointments/queue`
* **Headers**: `Authorization: Bearer {{token}}`, `Content-Type: application/json`
* **Body (raw JSON)**:
  ```json
  {
    "doctorId": "75c0b54a-ad66-4d6b-b5b8-7916bee586e3",
    "appointmentDate": "2024-04-01",
    "reasonForVisit": "Routine Checkup"
  }
  ```
* **Expected Response**: `201 Created`

---

## 3. Doctor Management (Requires Doctor Token)
*(Note: To test these endpoints, you MUST log in with a doctor account and use its returned `token`. Example: `email: asanka.bandara@caresync.lk`)*

### 3.1 Get Doctor Schedule
* **Method & URL**: `GET {{base_url}}/api/doctors/schedule`
* **Headers**: `Authorization: Bearer {{token}}`
* **Expected Response**: `200 OK`

### 3.2 Update Working Hours
* **Method & URL**: `PUT {{base_url}}/api/doctors/availability/working-hours`
* **Headers**: `Authorization: Bearer {{token}}`, `Content-Type: application/json`
* **Body (raw JSON)**:
  ```json
  {
    "workingDays": ["Monday", "Wednesday", "Friday"],
    "startTime": "09:00",
    "endTime": "17:00",
    "slotDuration": 30
  }
  ```
* **Expected Response**: `200 OK`

### 3.3 Get Today's Appointments
* **Method & URL**: `GET {{base_url}}/api/doctors/appointments/today`
* **Headers**: `Authorization: Bearer {{token}}`
* **Expected Response**: `200 OK`

---

## 4. Appointment Management

### 4.1 Get Available Slots
* **Method & URL**: `GET {{base_url}}/api/appointments/slots/75c0b54a-ad66-4d6b-b5b8-7916bee586e3?date=2024-04-01`
* **Headers**: `Authorization: Bearer {{token}}`
* **Expected Response**: `200 OK`

### 4.2 Create New Scheduled Appointment
* **Method & URL**: `POST {{base_url}}/api/appointments`
* **Headers**: `Authorization: Bearer {{token}}`, `Content-Type: application/json`
* **Body (raw JSON)**:
  ```json
  {
    "doctorId": "75c0b54a-ad66-4d6b-b5b8-7916bee586e3",
    "appointmentDate": "2024-04-01",
    "startTime": "10:00",
    "endTime": "10:30",
    "type": "consultation",
    "reason": "Routine checkup"
  }
  ```
* **Expected Response**: `201 Created`

### 4.3 Confirm Appointment (For Doctors)
* **Method & URL**: `PATCH {{base_url}}/api/appointments/789/confirm`
* **Headers**: `Authorization: Bearer {{token}}`
* **Expected Response**: `200 OK`

---

## 5. Medical Reports

### 5.1 Upload Medical Report
* **Method & URL**: `POST {{base_url}}/api/medical-reports/upload`
* **Headers**: `Authorization: Bearer {{token}}`
* **Body (form-data)**: 
  - Change to `form-data` in Body
  - Key: `file`, Type: `File`, Value: *(Select a sample PDF or image)*
  - Key: `patientId`, Type: `Text`, Value: `456`
  - Key: `doctorId`, Type: `Text`, Value: `75c0b54a-ad66-4d6b-b5b8-7916bee586e3`
  - Key: `recordType`, Type: `Text`, Value: `Lab Result`
  - Key: `description`, Type: `Text`, Value: `Monthly blood test results`
* **Expected Response**: `201 Created`

### 5.2 Get Medical Reports
* **Method & URL**: `GET {{base_url}}/api/medical-reports`
* **Headers**: `Authorization: Bearer {{token}}`
* **Expected Response**: `200 OK`

---

## 6. Admin Management (Requires Admin Token)

### 6.1 Get All Users
* **Method & URL**: `GET {{base_url}}/api/admin/users`
* **Headers**: `Authorization: Bearer {{token}}`
* **Expected Response**: `200 OK`

### 6.2 Approve Doctor
* **Method & URL**: `PATCH {{base_url}}/api/admin/doctors/75c0b54a-ad66-4d6b-b5b8-7916bee586e3/approval`
* **Headers**: `Authorization: Bearer {{token}}`, `Content-Type: application/json`
* **Body (raw JSON)**:
  ```json
  {
    "status": "approved"
  }
  ```
* **Expected Response**: `200 OK`

### 6.3 System Health Check
* **Method & URL**: `GET {{base_url}}/health`
* **Headers**: None required
* **Expected Response**: `200 OK`
  ```json
  {
    "status": "OK",
    "timestamp": "2024-03-21T10:00:00.000Z",
    "uptime": 123.456,
    "environment": "development"
  }
  ```
  }
  ```
