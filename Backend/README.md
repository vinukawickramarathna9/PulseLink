# PulseLink Backend

The backend for PulseLink, built with Node.js, Express, and SQL. 

## Setup Instructions

1. **Navigate to the Backend directory:**
   ```bash
   cd Backend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```
   *(Note: Ensure you have Node.js and npm installed on your system.)*

3. **Environment Setup:**
   - Create a `.env` file in the root of the `Backend/` directory.
   - Configure the required environment variables (e.g., Database credentials for `config/mysql.js`, PORT, Secret Keys, etc.).

4. **Database Migrations:**
   Ensure your SQL database (e.g., MySQL) is running and apply the necessary initial schema and updates from the `migrations/` folder.

5. **Start the server:**
   ```bash
   npm start
   ```
   *(For development with auto-reloading, run `npm run dev` if configured in package.json.)*

The API will now be running and ready to accept requests from the frontend or ML components.
