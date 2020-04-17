from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from phe import paillier

from e_vote.auth import login_required
from e_vote.db import get_db

bp = Blueprint('admin', __name__,url_prefix='/admin')

@bp.route('/admin_home')
def admin_home():
    return render_template('admin/admin_home.html')

@bp.route('/election_register')
def election_register():
    db = get_db()
    posts = db.execute(
        'SELECT p.author_id, title, body, created, username'
        ' FROM election_info p JOIN admin x ON p.author_id = x.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('admin/election_register.html', posts=posts)

@bp.route('/create_election', methods=('GET', 'POST'))
@login_required
def create_election():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO election_info (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('admin.create_election'))

    return render_template('admin/create_election.html')

@bp.route('/push_vote')
def push_vote():
    db = get_db()
    posts = db.execute(
        'SELECT p.author_id, title, created, username'
        ' FROM election_info p JOIN admin x ON p.author_id = x.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('admin/push_vote.html', posts=posts)

@bp.route('/candidate')
def candidate():
    db = get_db()
    posts = db.execute(
        'SELECT candidate_id, candidate_name, discription'
        ' FROM candidate_list'
    ).fetchall()
    return render_template('admin/candidate.html', posts=posts)

@bp.route('/vote')
def vote():
    db = get_db()
    posts = db.execute(
        'SELECT p.author_id, title, created, username'
        ' FROM election_info p JOIN admin x ON p.author_id = x.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('admin/vote.html', posts=posts)

@bp.route('/votelist')
def votelist():
    db = get_db()

    c1 = 1
    c2 = 10
    c3 = 100

    pk, sk = paillier.generate_paillier_keypair()
    e1=pk.encrypt(c1)
    e2=pk.encrypt(c2)
    e3=pk.encrypt(c3)

    db.execute(
        'INSERT INTO vote (voter_id, election_number, num)'
        ' VALUES (?, ?, ?)',
        (34010, 2, e1)
    )
    db.commit()

    return render_template('admin/vote.html')

@bp.route('/result')
def result():
    return render_template('admin/result.html')