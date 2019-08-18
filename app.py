from database.config import db
from flask import (
    flash,
    Flask,
    make_response,
    redirect,
    render_template,
    request
)
from flaskext.mysql import MySQL
import json
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(10)
app.config['MYSQL_DATABASE_HOST'] = db['host']
app.config['MYSQL_DATABASE_USER'] = db['user']
app.config['MYSQL_DATABASE_PASSWORD'] = db['password']
app.config['MYSQL_DATABASE_DB'] = db['name']

mysql = MySQL()
mysql.init_app(app)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")


@app.route('/')
def home():
    return render_template("add-student-info.html")


@app.route('/fetch_student/<name>', methods=['POST'])
def fetch_student(name):
    cur = mysql.connect().cursor()
    q = "SELECT `id` FROM `students` WHERE `name`=%s"
    cur.execute(q, name)
    res = cur.fetchone()

    if res:
        resp = json.dumps({
            "out": res[0],
            "status_code": "pass"
        })
        return resp

    resp = json.dumps({
        "out": "Error - match not found",
        "status_code": "fail"
    })
    return resp


@app.route('/submit', methods=['POST'])
def submit():

    # Prepare a mutable dict of `request.form`
    form = {}
    for key in request.form.keys():
        form[key] = request.form[key]
    
    # Set all empty strings to '0'
    for key in form.keys():
        if form[key] == '':
            form[key] = '0'

    name = form['name']
    ao1_a1 = form['ao1-a1']
    ao1_a2 = form['ao1-a2']
    ao1_a3 = form['ao1-a3']
    ao2_a1 = form['ao2-a1']
    ao2_a2 = form['ao2-a2']
    ao2_a3 = form['ao2-a3']
    ao3_a1 = form['ao3-a1']
    ao3_a2 = form['ao3-a2']
    ao3_a3=  form['ao3-a3']

    try:
        conn = mysql.connect()
        cur = conn.cursor()
        q = """
INSERT INTO scores (student_id,
                    ao1_a1, ao1_a2, ao1_a3,
                    ao2_a1, ao2_a2, ao2_a3,
                    ao3_a1, ao3_a2, ao3_a3)
VALUES (
    (SELECT id FROM students WHERE name=%s),
    %s, %s, %s, %s, %s, %s, %s, %s, %s
);
        """
        cur.execute(q, (name,
                        ao1_a1, ao1_a2, ao1_a3,
                        ao2_a1, ao2_a2, ao2_a3,
                        ao3_a1, ao3_a2, ao3_a3))
        conn.commit()
    except:
        return render_template("error.html")

    flash("Last feedback was successfully submitted.")
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
