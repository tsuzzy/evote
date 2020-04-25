from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from phe import paillier
from datetime import datetime
from e_vote.auth import login_required
from e_vote.db import get_db

bp = Blueprint('admin', __name__,url_prefix='/admin')

@bp.route('/admin_home')
def admin_home():
    return render_template('admin/admin_home.html')

@bp.route('/election_register')
def election_register():
    startTime = datetime.now()
    db = get_db()
    posts = db.execute(
        'SELECT p.author_id, title, body, created, username'
        ' FROM election_info p JOIN admin x ON p.author_id = x.id'
        ' ORDER BY created DESC'
    ).fetchall()
    print(datetime.now() - startTime)
    return render_template('admin/election_register.html', posts=posts)

@bp.route('/create_election', methods=('GET', 'POST'))
@login_required
def create_election():
    if request.method == 'POST':
        startTime = datetime.now()
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
            print(datetime.now() - startTime)
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
        'SELECT candidate_id, candidate_name, discription, election_number'
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


@bp.route('/result')
def result():
    db = get_db()
    data = db.execute(
        'SELECT num FROM vote WHERE election_number=1'
    ).fetchall()      #return a multi-dimension list, as ([],[],[])
    numlist = []
    for x in data:
        numlist.append(x[0]) #retrive the first value in each sub-list

    public_key,private_key = paillier.generate_paillier_keypair()
    encrypted_numlist = [public_key.encrypt(x) for x in numlist]

    sum = 0
    for i in encrypted_numlist:
        sum += i

    decrypted_sum = private_key.decrypt(sum)

    re = []
    while decrypted_sum != 0:
        remain = decrypted_sum % 10
        re.append(remain)
        decrypted_sum /= 10

    for i in re:
        db.execute(
            'INSERT INTO result (election_number, candidate, result)'
            'VALUES (?, ?, ?)',
            ()
        )

    print(decrypted_sum)

    return render_template('admin/result.html')