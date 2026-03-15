# PulseLink Frontend

The frontend user interface for PulseLink dashboard, built with React and Vite.

## Setup Instructions

1. **Navigate to the Frontend directory:**
   ```bash
   cd Frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```
   *(Note: Ensure you have Node.js and npm installed on your system.)*

3. **Environment Variables:**
   - Create a `.env` or `.env.local` file if required, pointing to your local backend and ML API URLs.

4. **Start the development server:**
   ```bash
   npm run dev
   ```
   This will start the Vite development server (usually on `http://localhost:5173/`).

## Building for Production

To build the frontend for production, run:
```bash
npm run build
```
The optimized bundle will be generated in the `dist` folder.
