import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash,generate_password_hash
from e_vote.db import get_db
bp=Blueprint('auth', __name__, url_prefix='/auth')

# Users Register -- Voter, Candidate, Election Authority
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        id_number=request.form['id_number']
        realname=request.form['realname']
        type=request.form.get('type_select')
        db=get_db()
        error=None

        # error config
        if not type:
            error='You must select one identity type.'
        elif type=='voter':
            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            elif not id_number:
                error = 'ID Number is required.'
            elif not realname:
                error = 'Real Name is required.'
            elif db.execute(
                    'SELECT vid FROM voter WHERE vid=?',
                    (id_number,)
            ).fetchone() is not None:
                error = 'User {} is already registered.'.format(realname)
        elif type=='candidate':
            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            elif not id_number:
                error = 'ID Number is required.'
            elif not realname:
                error = 'Real Name is required.'
            elif db.execute(
                    'SELECT cid FROM candidate WHERE cid=?',
                    (id_number,)
            ).fetchone() is not None:
                error = 'User {} is already registered.'.format(realname)
        elif type=='EA':
            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            elif not id_number:
                error = 'ID Number is required.'
            elif not realname:
                error = 'Real Name is required.'
            elif db.execute(
                    'SELECT EAid FROM election_authority WHERE EAid=?',
                    (id_number,)
            ).fetchone() is not None:
                error = 'User {} is already registered.'.format(realname)

        # Register
        if error is None:
            if type=='voter':
                db.execute(
                    'INSERT INTO voter (username,password,vid,vname) VALUES (?,?,?,?)',
                    (username,generate_password_hash(password),id_number,realname)
                )
                db.commit()
                return redirect(url_for('auth.login'))
            elif type=='candidate':
                db.execute(
                    'INSERT INTO candidate (username,password,cid,cname) VALUES (?,?,?,?)',
                    (username,generate_password_hash(password),id_number,realname)
                )
                db.commit()
                return redirect(url_for('auth.login'))
            elif type=='EA':
                db.execute(
                    'INSERT INTO election_authority (username,password,EAid,EAname) VALUES (?,?,?,?)',
                    (username, generate_password_hash(password),id_number,realname)
                )
                db.commit()
                return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


# Users login -- Voter, Candidate, Election Authority, System Authority

@bp.route('login',methods=('GET','POST'))
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        id_number=request.form['id_number']
        type = request.form.get('type_se lect')
        db=get_db()
        error=None

        if type=='voter':
            voter = db.execute(
                'SELECT * FROM voter WHERE vid=?', (id_number,)
            ).fetchone()
            if voter is None:
                error = 'Incorrect ID Number.'
            elif not check_password_hash(voter['password'], password):
                error = 'Incorrect password.'

            if error is None:
                session.clear()

                return redirect(url_for('index'))

            flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user=None
    else:
        g.user=get_db().execute(
            'SELECT * FROM user WHERE id = ?',(user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view