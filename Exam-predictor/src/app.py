from flask import Flask, render_template, request
import os
import joblib
import random
from datetime import date

# Load exam predictor model
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'exam_predictor.pkl')
model = joblib.load(model_path)

# Initialize Flask app
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

attendance_file = os.path.join(os.path.dirname(__file__), '..', 'attendance_log.txt')

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

# --- AI Knowledge Base ---
KNOWLEDGE_BASE = {
    "photosynthesis": "Photosynthesis is the process by which plants use sunlight, water, and carbon dioxide to create oxygen and energy in the form of sugar.",
    "gravity": "Gravity is the force that pulls objects toward each other. Sir Isaac Newton formulated the Law of Universal Gravitation after observing an apple fall.",
    "python": "Python is a high-level, interpreted programming language known for its readability and versatile libraries for data science and AI.",
    "algebra": "Algebra is a branch of mathematics where variables represent numbers in equations to solve for unknown values.",
    "gandhi": "Mahatma Gandhi was the leader of India's non-violent independence movement against British rule.",
    "evaporation": "Evaporation is the process of a liquid turning into a gas, typically when heated.",
    "democracy": "Democracy is a system of government where the citizens exercise power by voting for representatives.",
    "mitochondria": "Mitochondria are the powerhouses of the cell, generating chemical energy (ATP) for the cell's activities.",
    "calculus": "Calculus is the mathematical study of continuous change, focusing on derivatives (rates of change) and integrals (accumulation).",
    "osmosis": "Osmosis is the spontaneous movement of solvent molecules through a semi-permeable membrane into a region of higher solute concentration.",
    "capital of india": "The capital of India is New Delhi, located in the north-central part of the country.",
    "new delhi": "New Delhi is the capital city of India and the seat of its three branches of government.",
    "periodic table": "The periodic table organizes all known chemical elements by atomic number, electron configuration, and chemical properties.",
    "atom": "An atom is the basic unit of a chemical element, consisting of a nucleus (protons and neutrons) and electrons.",
    "molecule": "A molecule is a group of two or more atoms held together by chemical bonds.",
    "cell": "The cell is the basic structural, functional, and biological unit of all known organisms.",
    "dna": "DNA (Deoxyribonucleic acid) is the molecule that carries genetic instructions for development, functioning, and reproduction.",
    "earthquake": "An earthquake is the shaking of the Earth's surface caused by a sudden release of energy in the lithosphere.",
    "volcano": "A volcano is a rupture in the crust of a planetary-mass object that allows hot lava and volcanic gases to escape.",
    "tropic of cancer": "The Tropic of Cancer is the circle of latitude that contains the point where the Sun is directly overhead at the June solstice.",
    "world war 1": "WWI (1914–1918) was a global conflict centered in Europe between the Allied and Central Powers.",
    "world war 2": "WWII (1939–1945) was a global war that involved the vast majority of the world's countries and two opposing military alliances: the Allies and the Axis.",
    "shakespeare": "William Shakespeare was an English playwright, poet, and actor, widely regarded as the greatest writer in the English language.",
    "einstein": "Albert Einstein was a theoretical physicist who developed the theory of relativity and is famous for the equation E=mc².",
    "renaissance": "The Renaissance was a fervent period of European cultural, artistic, political, and economic 'rebirth' following the Middle Ages.",
    "solar system": "Our solar system consists of the Sun and everything bound to it by gravity—the planets, moons, asteroids, and comets.",
    "black hole": "A black hole is a region of spacetime where gravity is so strong that nothing, including light, can escape.",
    "artificial intelligence": "AI is the simulation of human intelligence processes by machines, especially computer systems.",
    "machine learning": "Machine learning is a subset of AI that uses algorithms to parse data, learn from it, and then make predictions or decisions.",
    "cloud computing": "Cloud computing is the on-demand availability of computer system resources, especially data storage and computing power.",
    "greenhouse effect": "The greenhouse effect is the process by which radiation from a planet's atmosphere warms the planet's surface.",
    "sustainable energy": "Sustainable energy is energy that is consumed at insignificant rates compared to its supply and with manageable side effects.",
    "global warming": "Global warming is the long-term heating of Earth's climate system observed since the pre-industrial period.",
    "economics": "Economics is the social science that studies how people interact with value—specifically, the production, distribution, and consumption of goods.",
    "inflation": "Inflation is the rate at which the general level of prices for goods and services is rising and, consequently, purchasing power is falling.",
    "constitution": "A constitution is an aggregate of fundamental principles or established precedents that constitute the legal basis of a polity.",
    "human rights": "Human rights are moral principles or norms for certain standards of human behavior and are regularly protected as legal rights.",
    "computer science": "Computer science is the study of computation, information, and automation.",
    "binary": "Binary code is a 2-symbol system using '0' and '1' to represent text, computer processor instructions, or any other data.",
    "software": "Software is a collection of instructions and data that tell a computer how to work.",
    "hardware": "Hardware refers to the physical elements that make up a computer or electronic system.",
    "internet": "The internet is a global system of interconnected computer networks that use the standard Internet protocol suite (TCP/IP).",
    "web browser": "A web browser is a software application for accessing information on the World Wide Web.",
    "coding": "Coding is the process of using a programming language to give a computer instructions on what to do.",
    "algorithm": "An algorithm is a finite sequence of rigorous instructions, typically used to solve a class of specific problems or perform a computation.",
}

def get_ai_answer(question):
    # Clean the question
    question = question.lower().strip()
    words = question.split()
    
    # Ranking logic: Find the best match based on keyword presence
    best_match = None
    max_count = 0
    
    for key, value in KNOWLEDGE_BASE.items():
        # Check if the key (entire phrase) is in the question
        if key in question:
            return value # High priority for exact phrase match
            
    # If no exact phrase, look for key words
    for key, value in KNOWLEDGE_BASE.items():
        key_words = key.split()
        match_count = sum(1 for kw in key_words if kw in words)
        
        if match_count > max_count:
            max_count = match_count
            best_match = value
            
    if max_count > 0:
        return best_match

    return None

# --- Smart Tutor (keyword-based) ---
@app.route("/tutor", methods=["GET", "POST"])
def tutor():
    if request.method == "POST":
        question = request.form["question"]
        answer = get_ai_answer(question)

        if not answer:
            answer = "I don't have a direct answer for that yet, but it's a great topic to research! Try asking about 'photosynthesis', 'gravity', or 'AI'."

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
    score = min(100, (word_count // 5) + 40 if word_count > 0 else 0)
    feedback = "Good effort! Try to expand your ideas to at least 100 words." if word_count < 100 else "EXCELLENT! Well-developed essay with sufficient depth."
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

    if os.path.exists(attendance_file):
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
        overall = "Present" if any(s == "Present" for s in slots.values()) else "Absent"
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
    question = request.form["question"]
    answer = get_ai_answer(question)

    if not answer:
        answer = "I'm still learning! For now, I can help with fundamental concepts in Science, Tech, and History. Try asking 'What is AI?'"

    return render_template("qa_result.html", question=question, answer=answer)

if __name__ == "__main__":
    app.run(debug=True)