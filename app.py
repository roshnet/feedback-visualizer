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
    return render_template("index.html")


@app.route('/feedback')
def feedback():
    return render_template("add-student-info.html")


@app.route('/viewall')
def viewall():
    cur = mysql.connect().cursor()
    q = """
SELECT name, ao1_a1, ao1_a2, ao1_a3, ao2_a1, ao2_a2, ao2_a3, ao3_a1, ao3_a2, ao3_a3
FROM scores
INNER JOIN students
ON scores.student_id = students.id;
    """
    cur.execute(q)
    rows = cur.fetchall()

    # Create a template parsable dict
    fields = [x[0] for x in cur.description]
    records = []
    for row in rows:
        rec = {}
        for i in range(len(fields)):
            rec[fields[i]] = row[i]
        records.append(rec)

    return render_template("submissions.html", students=records)


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
INSERT INTO students (name) VALUES (%s);
        """
        cur.execute(q, (name))
        conn.commit()

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
    return redirect('/feedback')


if __name__ == "__main__":
    app.run(debug=True)
