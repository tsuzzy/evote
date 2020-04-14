from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

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
        'SELECT p.author_id, title, body, created, username'
        ' FROM election_info p JOIN admin x ON p.author_id = x.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('user/notif.html', posts=posts)

# @bp.route('/insert_info',methods=('GET', 'POST'))
# @login_required
# def insert_info():
#     if request.method == 'POST':
#         name = request.form['name']
#         id = request.form['id']
#         body = request.form['body']
#         error = None
#
#         if not name:
#             error = 'Name is required.'
#         elif not id:
#             error = 'ID is required.'
#
#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'INSERT INTO candidate_list(candidate_id, candidate_name, discription)'
#                 ' VALUES (?, ?, ?)',
#                 (name, id, body)
#             )
#             db.commit()
#             return redirect(url_for('user.insert_info'))