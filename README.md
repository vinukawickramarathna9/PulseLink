# PulseLink

PulseLink is a comprehensive healthcare management system that integrates a backend API, a frontend dashboard, and a machine learning service for diabetes prediction.

## Project Structure

- **Backend/**: Node.js/Express REST API serving as the main backend for PulseLink.
- **Frontend/**: React/Vite-based user interface for doctors, patients, and admins.
- **Diabetes-Prediction/**: Python machine learning system and API for predicting diabetes risk.

## General Setup Instructions

To get the full project running locally, you will need to set up and run each of the three main components independently. Detailed setup instructions can be found in their respective directories:

1. **Backend**: Navigate to `Backend/`, install dependencies with `npm install`, set your environment variables, and start the node server. ([Backend Setup](Backend/README.md))
2. **Frontend**: Navigate to `Frontend/`, install dependencies with `npm install`, and start the development server. ([Frontend Setup](Frontend/README.md))
3. **Diabetes-Prediction**: Navigate to `Diabetes-Prediction/`, set up a Python virtual environment, install requirements from `requirements.txt`, and run the Python API. ([Diabetes Prediction Setup](Diabetes-Prediction/README.md))

Please refer to each component's `README.md` for more complete instructions.