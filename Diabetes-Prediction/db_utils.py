import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    host = os.getenv('MYSQL_HOST')
    port = int(os.getenv('MYSQL_PORT') or 3306)
    user = os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_PASSWORD')
    database = os.getenv('MYSQL_DATABASE')

    if not all([host, user, password, database]):
        raise RuntimeError('Missing MySQL environment variables (MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)')

    conn = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        autocommit=True,
    )
    return conn


def fetch_recent_predictions(limit=10):
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT 
              id,
              patient_id AS patientId,
              pregnancies,
              glucose,
              bmi,
              age,
              insulin,
              prediction_result AS predictionResult,
              prediction_probability AS predictionProbability,
              risk_level AS riskLevel,
              status,
              created_at AS createdAt,
              processed_at AS processedAt
            FROM diabetes_predictions
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (int(limit),)
        )
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()
