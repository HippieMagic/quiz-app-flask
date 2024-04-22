from flask import Flask, render_template, request, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from random import shuffle
import time
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'q'}
app.config['LOG_FILE'] = 'results.log'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


class QuizQuestion:
    def __init__(self, question_text, answers, correct_answer_index):
        self.question_text = question_text
        self.answers = answers
        self.correct_answer_index = correct_answer_index

    def to_dict(self):
        return {
            'question_text': self.question_text,
            'answers': self.answers,
            'correct_answer_index': self.correct_answer_index
        }

    @staticmethod
    def from_dict(data):
        return QuizQuestion(data['question_text'], data['answers'], data['correct_answer_index'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def log_results(score, total_questions):
    with open(app.config['LOG_FILE'], 'a') as file:
        file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Score: {score}/{total_questions}\n")


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
        num_questions = int(request.form.get('num_questions', 10))
        time_limit = int(request.form.get('time_limit', 180))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            all_questions = load_questions_from_file(file_path)
            shuffle(all_questions)

            if num_questions < len(all_questions):
                all_questions = all_questions[:num_questions]

            session['questions'] = [q.to_dict() for q in all_questions]
            session['total_questions'] = len(all_questions)
            session['score'] = 0
            session['current_question_index'] = 0
            session['start_time'] = time.time()
            session['time_limit'] = time_limit

            return redirect(url_for('question'))
    return render_template('upload.html')


def load_questions_from_file(file_path):
    questions = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

    current_question = None
    is_reading_question = False
    is_reading_answers = False

    for line in lines:
        line = line.strip()
        if not line or line.startswith("*"):
            continue

        if line.startswith("@Q"):
            is_reading_question = True
            current_question = QuizQuestion("", [], -1)
            continue

        if line.startswith("@A"):
            is_reading_question = False
            is_reading_answers = True
            continue

        if line.startswith("@E"):
            is_reading_answers = False
            questions.append(current_question)
            continue

        if is_reading_question:
            current_question.question_text += line + " "
        elif is_reading_answers:
            if line.isdigit():
                current_question.correct_answer_index = int(line) - 1
            else:
                current_question.answers.append(line)

    return questions


@app.route('/question', methods=['GET', 'POST'])
def question():
    if 'start_time' in session and (time.time() - session['start_time']) > session['time_limit']:
        return redirect(url_for('results'))

    if 'questions' not in session or 'current_question_index' not in session:
        flash('No quiz in progress. Please start a new quiz.')
        return redirect(url_for('home'))

    questions = [QuizQuestion.from_dict(q) for q in session['questions']]
    current_index = session['current_question_index']

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        if user_answer:
            correct_answer = questions[current_index].correct_answer_index
            if int(user_answer) == correct_answer:
                session['score'] += 1
            session['current_question_index'] += 1

        return redirect(url_for('question'))

    if current_index < len(questions):
        current_question = questions[current_index]
        answers_with_index = list(enumerate(current_question.answers))
        time_left = session['start_time'] + session['time_limit'] - time.time()
        return render_template('question.html', question=current_question.question_text,
                               answers=answers_with_index, question_number=current_index + 1,
                               time_limit=time_left if time_left > 0 else 0)
    else:
        return redirect(url_for('results'))


@app.route('/results')
def results():
    score = session.get('score', 0)
    total_questions = session.get('total_questions', 0)
    log_results(score, total_questions)
    recent_result = f"Most Recent - Score: {score}/{total_questions} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    session.clear()
    return redirect(url_for('view_results', recent_result=recent_result))


@app.route('/view_results')
def view_results():
    recent_result = request.args.get('recent_result', 'No recent results.')
    try:
        with open(app.config['LOG_FILE'], 'r') as file:
            results = file.readlines()
    except FileNotFoundError:
        results = ["No past results recorded yet."]
    return render_template('view_results.html', results=results, recent_result=recent_result)


if __name__ == '__main__':
    app.run(debug=True)
