from flask import Flask, render_template, request
import os
import joblib
import random
from datetime import date

# Load exam predictor model
model = joblib.load("models/exam_predictor.pkl")

# Initialize Flask app
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

attendance_file = "attendance_log.txt"

# --- Dashboard ---
@app.route("/")
def home():
    return render_template("index.html")

# --- Exam Predictor ---
@app.route("/predictor")
def predictor():
    return render_template("predictor.html")

@app.route("/predict", methods=["POST"])
def predict():
    study_hours = float(request.form["study_hours"])
    attendance = float(request.form["attendance"])
    past_scores = float(request.form["past_scores"])

    prediction = model.predict([[study_hours, attendance, past_scores]])[0]
    prediction_text = f"Predicted Exam Score: {prediction:.2f}"

    return render_template("result.html", prediction_text=prediction_text)

# --- Smart Tutor (keyword-based) ---
@app.route("/tutor", methods=["GET", "POST"])
def tutor():
    if request.method == "POST":
        question = request.form["question"].lower()

        answers = {
            "photosynthesis": "Photosynthesis is the process by which plants use sunlight to make food.",
            "gravity": "Sir Isaac Newton discovered gravity when he observed an apple falling.",
            "python": "Python is a programming language known for simplicity and readability.",
            "algebra": "Algebra is a branch of mathematics dealing with symbols and rules.",
            "gandhi": "Mahatma Gandhi was a leader of India's independence movement, known for non-violence.",
            "evaporation": "Evaporation is when liquid water turns into vapor due to heat.",
            "democracy": "Democracy is a system of government where citizens exercise power by voting.",
            "mitochondria": "Mitochondria are organelles that produce energy in cells.",
            "calculus": "Calculus studies continuous change using derivatives and integrals.",
            "osmosis": "Osmosis is the movement of water through a semi-permeable membrane.",
            "capital of india": "The capital of India is New Delhi.",
            "new delhi": "The capital of India is New Delhi.",
            "name": "I’m your Smart Tutor, here to help you learn!"
        }

        answer = None
        for key, val in answers.items():
            if key in question:
                answer = val
                break

        if not answer:
            answer = "That's a great question! I don’t have a direct answer yet, but you can research it step by step."

        tip = random.choice([
            "Review your notes daily for better retention.",
            "Practice with past exam papers.",
            "Teach the concept to a friend to test your understanding.",
            "Use flashcards for quick revision.",
            "Break study sessions into smaller chunks for focus."
        ])

        return render_template("tutor_result.html", question=question, answer=answer, tip=tip)

    return render_template("tutor.html")

# --- Essay Grader ---
@app.route("/essay")
def essay():
    return render_template("essay.html")

@app.route("/grade_essay", methods=["POST"])
def grade_essay():
    essay_text = request.form["essay_text"]
    word_count = len(essay_text.split())
    score = min(100, word_count)
    feedback = "Good effort! Try to expand your ideas." if word_count < 50 else "Well-developed essay with sufficient length."
    return render_template("essay_result.html", score=score, feedback=feedback)

# --- Attendance System (slot-wise, date-wise) ---
@app.route("/attendance")
def attendance():
    return render_template("attendance.html")

@app.route("/attendance_log", methods=["GET", "POST"])
def attendance_log():
    today = str(date.today())
    records = {}

    if request.method == "POST":
        roll_no = request.form["roll_no"]
        student_name = request.form["student_name"]
        slot = request.form["slot"]
        status = request.form["status"]

        with open(attendance_file, "a") as f:
            f.write(f"{today},{roll_no},{student_name},{status},{slot}\n")

    with open(attendance_file, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 5:
                rec_date, roll_no, student_name, status, slot = parts
                if rec_date == today:
                    if roll_no not in records:
                        records[roll_no] = {"student_name": student_name, "slots": {}}
                    records[roll_no]["slots"][slot] = status

    summary = []
    for roll_no, data in records.items():
        slots = data["slots"]
        overall = "Present" if all(s == "Present" for s in slots.values()) else "Absent"
        summary.append({
            "roll_no": roll_no,
            "student_name": data["student_name"],
            "overall": overall,
            "slots": slots
        })

    return render_template("attendance_log.html", records=summary)

# --- QA Bot (keyword-based) ---
@app.route("/qa")
def qa():
    return render_template("qa.html")

@app.route("/qa_answer", methods=["POST"])
def qa_answer():
    question = request.form["question"].lower()

    answers = {
        "capital": "Capitals are the main cities of countries. For example, India’s capital is New Delhi.",
        "python": "Python is a programming language great for beginners and powerful for professionals.",
        "math": "Math is about problem solving. Break problems into smaller steps."
    }

    answer = None
    for key, val in answers.items():
        if key in question:
            answer = val
            break

    if not answer:
        answer = "That's an interesting question! Try breaking it down and researching step by step."

    return render_template("qa_result.html", question=question, answer=answer)

if __name__ == "__main__":
    app.run(debug=True)