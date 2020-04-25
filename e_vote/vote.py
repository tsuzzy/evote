from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from phe import paillier
from e_vote.db import get_db

bp = Blueprint('vote', __name__,url_prefix='/vote')

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

    for i in range(len(re)):
        db.execute(
            'INSERT INTO result (election_number, candidate, result)'
            'VALUES (?, ?, ?)',
            (election_number, i, re[i]/len(re))
        )

    print(decrypted_sum)

    return render_template('vote/result.html')