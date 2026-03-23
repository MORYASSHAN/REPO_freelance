from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for attendance (cleared when server restarts)
attendance_records = []

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Exam Predictor
@app.route('/exam-predictor', methods=['GET', 'POST'])
def exam_predictor():
    if request.method == 'POST':
        study_hours = float(request.form.get('study_hours', 0))
        attendance = float(request.form.get('attendance', 0))
        past_scores = float(request.form.get('past_scores', 0))
        
        # Simple formula: weights: study_hours 50%, attendance 30%, past_scores 20%
        predicted = (0.5 * study_hours) + (0.3 * attendance) + (0.2 * past_scores)
        predicted = round(predicted, 2)
        return render_template('exam_result.html', predicted=predicted)
    
    return render_template('exam_predictor.html')

# Smart Tutor
@app.route('/smart-tutor', methods=['GET', 'POST'])
def smart_tutor():
    if request.method == 'POST':
        # We don't store the question; just show a thank-you page
        return render_template('tutor_thanks.html')
    return render_template('smart_tutor.html')

# Automated Essay Grader
@app.route('/essay-grader', methods=['GET', 'POST'])
def essay_grader():
    if request.method == 'POST':
        essay = request.form.get('essay', '')
        word_count = len(essay.split())
        
        # Grading rubric based on word count
        if word_count < 50:
            grade = "Hollow Start"
            feedback = "Your essay is very short. Try to develop your ideas further."
        elif 50 <= word_count < 150:
            grade = "Developing"
            feedback = "Good start! Add more details and examples to strengthen your essay."
        elif 150 <= word_count < 300:
            grade = "Covered"
            feedback = "Well done! Your essay covers the main points effectively."
        else:
            grade = "Excellent"
            feedback = "Outstanding! Rich content and thorough exploration."
        
        return render_template('essay_result.html', word_count=word_count, grade=grade, feedback=feedback)
    
    return render_template('essay_grader.html')

# Mark Attendance
@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        roll_no = request.form.get('roll_no')
        student_name = request.form.get('student_name')
        slot = request.form.get('slot')
        status = request.form.get('status')
        
        # Store record
        attendance_records.append({
            'roll_no': roll_no,
            'student_name': student_name,
            'slot': slot,
            'status': status
        })
        return redirect(url_for('attendance'))  # reload the form
    
    return render_template('attendance.html')

@app.route('/attendance/view')
def attendance_view():
    return render_template('attendance_view.html', records=attendance_records)

# Smart QA Bot (placeholder)

@app.route('/qa-bot')
def qa_bot():
    return render_template('qa_bot.html')


if __name__ == '__main__':
    app.run(debug=True)