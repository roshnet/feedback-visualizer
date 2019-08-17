from database.config import db
from flask import (
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


# @app.errorhandler(404)
# def page_not_found():
#     return render_template("error.html")


@app.route('/')
def home():
    return render_template("add-student-info.html")


@app.route('/fetch_student/<name>', methods=['POST'])
def fetch_student(name):
    print("======================================")
    cur = mysql.connect().cursor()
    q = "SELECT `id` FROM `students` WHERE `name`=%s"
    cur.execute(q, name)
    res = cur.fetchone()

    if res:
        resp = json.dumps({
            "out": res[0],
            "status_code": 200
        })
        return resp

    resp = json.dumps({
        "out": "Error - match not found",
        "status_code": "400"
    })
    return resp


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    ao1_score = request.form['rate-ao1']
    ao2_score = request.form['rate-ao2']
    ao3_score = request.form['rate-ao3']

    try:
        conn = mysql.connect()
        cur = conn.cursor()
        q = """
INSERT INTO ratings (student_id, AO1, AO2, AO3)
VALUES (
    (SELECT id FROM students WHERE name=%s),
    %s, %s, %s
);
        """
        cur.execute(q, (name,
                        ao1_score,
                        ao2_score,
                        ao3_score))
        conn.commit()
    except:
        return render_template("error.html")

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
