from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///polls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'poll_secret_key'

db = SQLAlchemy(app)

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    is_multiple_choice = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    options = db.relationship('Option', backref='poll', cascade='all, delete', lazy=True)

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    votes = db.Column(db.Integer, default=0)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)

@app.route('/')
def index():
    polls = Poll.query.order_by(Poll.created_at.desc()).all()
    return render_template('index.html', polls=polls)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        question = request.form['question']
        is_multi = 'is_multiple_choice' in request.form
        options = request.form.getlist('options')

        new_poll = Poll(question=question, is_multiple_choice=is_multi)
        db.session.add(new_poll)
        db.session.commit()

        for opt in options:
            db.session.add(Option(text=opt, poll_id=new_poll.id))
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/vote/<int:poll_id>', methods=['POST'])
def vote(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    selected_option_ids = request.form.getlist('choice')

    for option_id in selected_option_ids:
        option = Option.query.filter_by(id=option_id, poll_id=poll.id).first()
        if option:
            option.votes += 1

    db.session.commit()
    return redirect(url_for('poll_results', poll_id=poll.id))

@app.route('/results/<int:poll_id>')
def poll_results(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    return render_template('results.html', poll=poll)

@app.route('/delete/<int:poll_id>', methods=['POST'])
def delete_poll(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    db.session.delete(poll)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
