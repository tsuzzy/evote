from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import math
from werkzeug.exceptions import abort
from datetime import datetime
from e_vote.auth import login_required
from e_vote.db import get_db

bp = Blueprint('user', __name__,url_prefix='/user')

@bp.route('/user_home')
def user_home():  #函数名必须和对应html名称相同！
    return render_template('user/user_home.html')


@bp.route('/notif')
def notif():
    db = get_db()
    posts = db.execute(
        'SELECT p.info_id, author_id, title, body, created, username'
        ' FROM election_info p JOIN admin x ON p.author_id = x.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('user/notif.html', posts=posts)


@bp.route('/enroll_form',methods=['GET', 'POST'])
@login_required
def enroll_form():
    db = get_db()
    if request.method == 'POST':

        startTime = datetime.now()
        name = request.form['name']
        candidate_id = request.form['candidate_id']
        info_id = request.form['info_id']
        body = request.form['body']
        error = None
        person = db.execute(
            'SELECT * FROM user WHERE user_id = ?',
            (candidate_id,)
        ).fetchone()

        if not name:
            error = '请填入姓名'
        elif not candidate_id:
            error = '请输入身份证号'
        elif not info_id:
            error = '请输入选举场次号码'
        elif person is None:
            error = '证件号码不正确'

        if error is not None:
            flash(error)
        else:
            db.execute(
                'INSERT INTO candidate_list (election_number, candidate_id, candidate_name, discription)'
                ' VALUES (?, ?, ?, ?)',
                (info_id, candidate_id, name, body)
            )
            db.commit()

            autoid = db.execute(
                'SELECT id FROM candidate_list WHERE candidate_id = ?',(candidate_id,)
            ).fetchone()
            i = autoid[0]
            calcu = math.pow(10, i-1)
            db.execute(
                'UPDATE candidate_list SET calcu_id=? WHERE id=?',
                (calcu,i)
            )
            db.commit()
            print(datetime.now() - startTime)
            return redirect(url_for('user.notif'))

    return render_template('user/enroll_form.html')


@bp.route('/votelist',methods = ('GET', 'POST'))
def votelist():
    startTime = datetime.now()
    db = get_db()
    posts = db.execute(
        'SELECT candidate_id, candidate_name, discription, election_number'
        ' FROM candidate_list'
    ).fetchall()
    user = db.execute(
        'SELECT * FROM user WHERE id = ?',
        (g.user['id'],)
    ).fetchone()
    person = db.execute(
        'SELECT candidate_id FROM candidate_list WHERE candidate_id = ?',
        (user[3],)
    ).fetchone()
    voter = db.execute(
        'SELECT * FROM vote WHERE voter_id = ?',
        (user[3],)
    ).fetchone()

    if request.method == 'POST':
        candidate_id = request.form['vote']
        error = None

        if not candidate_id:
            error = '请选择一位候选人。'
        elif person is not None:
            error = '您是候选人，不具备本场竞选投票资格。'
        elif voter is not None:
            error = '不可以重复投票。'
        flash(error)

        if error is None:
            candidateid = int(candidate_id)
            row = db.execute(
                'SELECT * FROM user WHERE id =?',
                (g.user['id'],)
            ).fetchone()
            user_id = row[3]

            row1 = db.execute(
                'SELECT * FROM candidate_list WHERE candidate_id = ?',
                (candidateid,)
            ).fetchone()
            calcu_id = row1[5]

            db.execute(
                'INSERT INTO vote (voter_id, election_number, num)'
                'VALUES (?, ?, ?)',
                (user_id, 2, calcu_id)
            )
            db.commit()
            print(datetime.now() - startTime)
        return redirect(url_for('user.votelist'))

    return render_template('user/votelist.html', posts=posts)