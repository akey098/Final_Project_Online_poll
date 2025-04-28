# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///polls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    is_multiple_choice = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    options = db.relationship(
        'Option', backref='poll', lazy=True,
        cascade='all, delete-orphan'
    )

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    votes = db.Column(db.Integer, default=0)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)

@app.route('/')
def index():
    polls = Poll.query.order_by(Poll.created_at.desc()).all()
    total_votes = sum(opt.votes for opt in Option.query.all())
    total_polls = Poll.query.count()
    return render_template(
        'base.html',
        polls=polls,
        total_votes=total_votes,
        total_polls=total_polls
    )

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        question = request.form['question']
        is_multiple_choice = 'is_multiple_choice' in request.form
        option_texts = request.form.getlist('options')
        if question and len(option_texts) >= 2:
            poll = Poll(
                question=question,
                is_multiple_choice=is_multiple_choice
            )
            db.session.add(poll)
            db.session.flush()
            for text in option_texts:
                db.session.add(Option(text=text, poll_id=poll.id))
            db.session.commit()
            return redirect(url_for('index'))

    total_votes = sum(opt.votes for opt in Option.query.all())
    total_polls = Poll.query.count()
    return render_template(
        'create.html',
        total_votes=total_votes,
        total_polls=total_polls
    )

@app.route('/vote/<int:poll_id>', methods=['POST'])
def vote(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    selected_option_ids = request.form.getlist('choice')
    for option_id in selected_option_ids:
        option = Option.query.filter_by(
            id=option_id, poll_id=poll.id
        ).first()
        if option:
            option.votes += 1
    db.session.commit()
    return redirect(
        url_for('poll_results', poll_id=poll.id,
                voted=selected_option_ids)
    )

@app.route('/results/<int:poll_id>')
def poll_results(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    total_votes = sum(option.votes for option in poll.options)
    total_polls = Poll.query.count()
    return render_template(
        'results.html',
        poll=poll,
        total_votes=total_votes,
        total_polls=total_polls
    )

# NEW: delete route
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
