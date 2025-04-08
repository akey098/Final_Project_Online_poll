from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///polls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Poll model
class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    option1 = db.Column(db.String(100), nullable=False)
    option2 = db.Column(db.String(100), nullable=False)
    votes1 = db.Column(db.Integer, default=0)
    votes2 = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Home route to display polls
@app.route('/')
def index():
    polls = Poll.query.order_by(Poll.created_at.desc()).all()
    return render_template('index.html', polls=polls)

# Create a new poll
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        question = request.form['question']
        option1 = request.form['option1']
        option2 = request.form['option2']
        new_poll = Poll(question=question, option1=option1, option2=option2)
        db.session.add(new_poll)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

# Vote on a poll
@app.route('/vote/<int:poll_id>', methods=['POST'])
def vote(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    choice = request.form['choice']
    if choice == 'option1':
        poll.votes1 += 1
    elif choice == 'option2':
        poll.votes2 += 1
    db.session.commit()
    return redirect(url_for('index'))

# Initialize DB and run app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
