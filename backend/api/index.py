from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os

app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing for Frontend hosting

# In-memory database simulation
USERS = {"admin@school.com": "password123"}
STUDENTS = [
    {"id": 1, "name": "Alice Smith", "attendance": 92, "marks": 88, "assignments": 85, "prediction": "High Performer", "report": ""},
    {"id": 2, "name": "Bob Jones", "attendance": 74, "marks": 55, "assignments": 60, "prediction": "Average Performer", "report": ""},
    {"id": 3, "name": "Charlie Brown", "attendance": 52, "marks": 42, "assignments": 45, "prediction": "At Risk", "report": ""}
]

# Load ML Model safely
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../student_model.pkl')
model = None
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)

def get_performance_string(category_code):
    mapping = {2: "High Performer", 1: "Average Performer", 0: "At Risk"}
    return mapping.get(category_code, "Unknown")

# Rule-based GenAI engine wrapper simulating LLM logic for quick, dynamic text responses
def generate_llm_report(name, attendance, marks, prediction):
    prompt_summary = f"The student {name} has {attendance}% attendance and an academic score of {marks}%. Our ML model classifies them as: {prediction}."
    
    if prediction == "High Performer":
        return f"{prompt_summary} Exceptional work! Demonstrates consistency across assignments and classes. Recommended to participate in advanced honors programs and peer mentorship."
    elif prediction == "Average Performer":
        return f"{prompt_summary} The student shows moderate attendance and average academic performance. Assignment scores are steady, but exam preparation could improve. Recommended to focus on targeted review sessions."
    else:
        return f"{prompt_summary} Critical attention required. Low attendance patterns directly correlate with weak test metrics. Immediate academic intervention, mandatory study hours, and parental updates are highly advised."

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if USERS.get(email) == password:
        return jsonify({"status": "success", "message": "Logged in successfully"}), 200
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

@app.route('/api/students', methods=['GET', 'POST'])
def manage_students():
    if request.method == 'GET':
        return jsonify(STUDENTS), 200
    
    if request.method == 'POST':
        data = request.json
        name = data.get('name')
        attendance = int(data.get('attendance'))
        marks = int(data.get('marks'))
        assignments = int(data.get('assignments'))
        
        # ML Prediction Engine fallback
        if model:
            pred_code = model.predict([[attendance, marks, assignments]])[0]
            prediction = get_performance_string(pred_code)
        else:
            prediction = "Average Performer" # Fallback if model pkl is missing
            
        new_student = {
            "id": len(STUDENTS) + 1,
            "name": name,
            "attendance": attendance,
            "marks": marks,
            "assignments": assignments,
            "prediction": prediction,
            "report": ""
        }
        STUDENTS.append(new_student)
        return jsonify(new_student), 201

@app.route('/api/students/<int:student_id>/report', methods=['POST'])
def generate_report(student_id):
    student = next((s for s in STUDENTS if s['id'] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404
        
    # GenAI Feature invocation
    ai_report = generate_llm_report(student['name'], student['attendance'], student['marks'], student['prediction'])
    student['report'] = ai_report
    return jsonify({"status": "success", "report": ai_report}), 200

# Vercel requirements
if __name__ == '__main__':
    app.run(debug=True, port=5000)