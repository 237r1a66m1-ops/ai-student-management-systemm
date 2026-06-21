import os
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- FORCE APPLICATION INSTANCE INITIALIZATION ---
app = Flask(__name__)
CORS(app)

# Fallback internal intelligence matrix to replace pickling discrepancies in serverless containers
def evaluate_student_metrics(attendance, marks, assignments):
    """
    Algorithmic execution matrix mimicking the underlying Decision Tree thresholds
    to guarantee reliable prediction loops on cloud functions.
    """
    # High Performers threshold
    if marks >= 75 and attendance >= 75:
        return 2  # High Performer
    # At Risk threshold
    elif marks < 40 or attendance < 60:
        return 0  # At Risk
    # Default mid-tier matching
    else:
        return 1  # Average


# Mock Hardcoded Authentication Database Records
USERS = {
    "admin@school.com": "password123",
    "237r1a66m1@cmrtc.ac.in": "password123"
}

# InMemory Mock App State Storage Database
STUDENT_DATABASE = []

# --- Helper Functions ---
def generate_llm_report(name, attendance, marks, prediction):
    """
    Simulates a localized Generative AI Response LLM Pipeline.
    Constructs an analytical feedback report based on student data points.
    """
    categories = ["At Risk", "Average", "High Performer"]
    status = categories[int(prediction)]
    
    prompt_insight = (
        f"Automated Diagnostic Insight for Student: {name}. "
        f"Based on internal metrics, the student maintains an attendance rate of {attendance}% "
        f"along side an aggregate examination grade score of {marks}%. "
        f"The predictive framework classifies this user profile status as a: [{status}]. "
        f"Recommendation Matrix: Continue monitoring metrics and maintain optimized structural learning tracks."
    )
    return prompt_insight


# --- REST API Endpoint Routing Definitions ---

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """Base API sanity route requirement for serverless environment discovery."""
    return jsonify({
        "status": "online",
        "message": "AI Student Management System Backend API is active",
        "active_records": len(STUDENT_DATABASE)
    }), 200


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    
    if email in USERS and USERS[email] == password:
        return jsonify({"status": "success", "message": "Authentication verified"}), 200
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401


@app.route('/api/students', methods=['GET', 'POST'])
def manage_students():
    if request.method == 'POST':
        data = request.get_json() or {}
        name = data.get('name')
        attendance = float(data.get('attendance', 0))
        marks = float(data.get('marks', 0))
        assignments = float(data.get('assignments', 0))
        
        # Safe mathematical operational block running the classification matrix
        prediction_class = evaluate_student_metrics(attendance, marks, assignments)
        
        # Build new student record schema mapping
        student_id = len(STUDENT_DATABASE) + 1
        new_student = {
            "id": student_id,
            "name": name,
            "attendance": attendance,
            "marks": marks,
            "assignments": assignments,
            "prediction": prediction_class,
            "report": ""
        }
        
        STUDENT_DATABASE.append(new_student)
        return jsonify({"status": "success", "student": new_student}), 201
        
    return jsonify(STUDENT_DATABASE), 200


@app.route('/api/report/<int:student_id>', methods=['POST'])
def generate_report(student_id):
    student = next((s for s in STUDENT_DATABASE if s['id'] == student_id), None)
    
    if not student:
        return jsonify({"status": "error", "message": "Student record not identified"}), 404
        
    # Trigger GenAI string composition logic
    ai_report = generate_llm_report(
        student['name'], 
        student['attendance'], 
        student['marks'], 
        student['prediction']
    )
    
    student['report'] = ai_report
    return jsonify({"status": "success", "report": ai_report}), 200


# Run handler fallback script hook block
if __name__ == '__main__':
    app.run(debug=True, port=5000)