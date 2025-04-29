from flask import Blueprint, render_template, request, redirect, url_for
from .models import Poll, Option
from . import db

polls_bp = Blueprint('polls', __name__)

@polls_bp.route('/')
def index():
    polls = Poll.query.order_by(Poll.created_at.desc()).all()
    total_votes = sum(opt.votes for opt in Option.query.all())
    total_polls = Poll.query.count()
    return render_template(
        'index.html',
        polls=polls,
        total_votes=total_votes,
        total_polls=total_polls
    )

@polls_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        question = request.form['question']
        is_multiple = 'is_multiple_choice' in request.form
        texts = request.form.getlist('options')
        if question and len(texts) >= 2:
            poll = Poll(question=question, is_multiple_choice=is_multiple)
            db.session.add(poll)
            db.session.flush()
            for txt in texts:
                db.session.add(Option(text=txt, poll_id=poll.id))
            db.session.commit()
            return redirect(url_for('polls.index'))
    total_votes = sum(opt.votes for opt in Option.query.all())
    total_polls = Poll.query.count()
    return render_template(
        'create.html',
        total_votes=total_votes,
        total_polls=total_polls
    )

@polls_bp.route('/vote/<int:poll_id>', methods=['POST'])
def vote(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    selected = request.form.getlist('choice')
    for oid in selected:
        opt = Option.query.filter_by(id=oid, poll_id=poll.id).first()
        if opt:
            opt.votes += 1
    db.session.commit()
    return redirect(
        url_for('polls.poll_results', poll_id=poll.id, voted=selected)
    )

@polls_bp.route('/results/<int:poll_id>')
def poll_results(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    total_votes = sum(o.votes for o in poll.options)
    total_polls = Poll.query.count()
    return render_template(
        'results.html',
        poll=poll,
        total_votes=total_votes,
        total_polls=total_polls
    )

@polls_bp.route('/delete/<int:poll_id>', methods=['POST'])
def delete_poll(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    db.session.delete(poll)
    db.session.commit()
    return redirect(url_for('polls.index'))
