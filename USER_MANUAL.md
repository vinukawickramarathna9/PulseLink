# PulseLink User Manual

Welcome to the **PulseLink** User Manual. PulseLink is a comprehensive Healthcare & Hospital Management System that integrates patient portals, doctor management, administrative controls, and an advanced Machine Learning module for Diabetes Prediction.

## Table of Contents
1. [Overview](#overview)
2. [User Roles and Features](#user-roles-and-features)
   - [Patients](#patients)
   - [Doctors](#doctors)
   - [Administrators](#administrators)
3. [System Architecture](#system-architecture)
4. [Getting Started (Installation & Running)](#getting-started-installation--running)
   - [Prerequisites](#prerequisites)
   - [Backend Setup](#backend-setup)
   - [Frontend Setup](#frontend-setup)
   - [Machine Learning Module Setup](#machine-learning-module-setup)
5. [API Documentation](#api-documentation)

---

## Overview
PulseLink is designed to streamline healthcare operations. It handles appointment scheduling, billing, insurance claims, medical records, and integrates AI-driven health predictions (specifically Diabetes prediction) to assist in proactive healthcare.

## User Roles and Features

### Patients
- **Authentication:** Secure registration and login.
- **Appointments:** Book, reschedule, or cancel appointments with doctors.
- **Medical Reports:** Access and view past medical reports and prescriptions securely.
- **Health Prediction:** Input health metrics into the Diabetes Prediction system to evaluate risk factors.
- **Billing & Insurance:** View invoices and track health insurance claims.

### Doctors
- **Dashboard:** View daily schedules and patient queues.
- **Manage Appointments:** Accept, mark as complete, or update appointment statuses.
- **Medical Records:** Create and update medical reports for patients post-consultation.

### Administrators
- **System Management:** Manage patient and doctor accounts.
- **Financials:** Oversee billing, invoicing, and process insurance claims.
- **Reporting:** Generate and view administrative reports (system usage, financial summaries).
- **Health Predictions Overview:** Access aggregated health prediction statistics.

---

## System Architecture
PulseLink is divided into three main components:
1. **Frontend:** Built with React/Vite and TypeScript, utilizing TailwindCSS for responsive UI.
2. **Backend:** A Node.js/Express REST API interfacing with databases (MongoDB/MySQL). It handles authentication, business logic, and database transactions.
3. **Diabetes-Prediction Module:** A Python-based Machine Learning API utilizing datasets to predict diabetes probability based on patient attributes.

---

## Getting Started (Installation & Running)

### Prerequisites
- **Node.js**: v16+ recommended
- **Python**: 3.8+ recommended
- **Databases**: MongoDB and/or MySQL server running locally or via cloud.

### Backend Setup
The backend serves the main API for the application.
1. Navigate to the Backend directory:
   ```bash
   cd Backend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Set up environment variables (ensure database URIs and JWT secrets are set in your `.env` file).
4. Run the server:
   ```bash
   npm run dev
   ```

### Frontend Setup
The frontend provides the user interface for Patients, Doctors, and Admins.
1. Navigate to the Frontend directory:
   ```bash
   cd Frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

### Machine Learning Module Setup
This module provides the prediction endpoints.
1. Navigate to the ML directory:
   ```bash
   cd Diabetes-Prediction
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the API (usually Flask/FastAPI based):
   ```bash
   python predict_api.py
   ```
   *(Check `Diabetes-Prediction/README.md` for specific ML training instructions.)*

---

## API Documentation
The backend includes a Swagger-based API documentation. Once the backend server is running, you can access the Swagger UI by navigating to:
`http://localhost:<PORT>/api/docs` (defaultly configured via the `docs/swagger.js` file).

For deployment guidelines, refer to `Backend/docs/DEPLOYMENT.md` and `Backend/docs/SSL_SETUP.md`.
