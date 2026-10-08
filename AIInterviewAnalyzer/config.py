import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ai_interview_analyzer"
)

cursor = db.cursor(dictionary=True)