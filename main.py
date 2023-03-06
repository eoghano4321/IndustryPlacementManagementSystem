import datetime

import oracledb
from flask import Flask, render_template, request

# Replace with your actual Oracle database credentials
user = 'SYSTEM'
password = 'root'
port = 1521
service_name = 'XE'
conn_string = "localhost:{port}/{service_name}".format(
    port=port, service_name=service_name)
app = Flask(__name__)
data = []
id = []

# get Job_Ids from Employee Table
connection = oracledb.connect(
    user=user, password=password, dsn=conn_string)
cur = connection.cursor()
job_id = cur.execute('select LOGIN_ID from IPMS.LOGIN')
for row in job_id:
    id.append(row[0])
cur.close()
connection.close()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/employee_view', methods=['GET', 'POST'])
def get_data():
    print("Getting")
    connection = oracledb.connect(
        user=user, password=password, dsn=conn_string)
    cur = connection.cursor()
    cur.execute('select * from IPMS.USERS')
    data.clear()
    for row in cur:
        data.append({"First_Name": row[2], "Last_Name": row[1],
                    "Login_ID": row[3], "USERTYPE_ID": row[4], "IS_PENDING": row[5], "IS_APPROVED": row[6]})
    # Close the cursor and connection
    cur.close()
    connection.close()

    return render_template('index.html', data=data, job_id=id)


@app.route('/placements_view',methods=['GET'])
def update():
    jobs = []
    connection = oracledb.connect(
        user=user, password=password, dsn=conn_string)
    cur = connection.cursor()
    cur.execute('SELECT PLACEMENT_ID, TITLE, SKILLS, DESCRIPTION FROM IPMS.PLACEMENTS')
    for row in cur:
        jobs.append({"PID": row[0], "PTitle": row[1],
                    "Skills": row[2], "Desc": row[3]})
    # Close the cursor and connection
    cur.close()
    connection.close()
    # Pass the data to the template to display in the HTML table
    return render_template('placements.html', data=jobs)
    #return render_template('about.html')


@app.route('/about_View')
def about():
    return render_template('about.html')


@app.route('/Insert_View')
def insert():
    return render_template('Insertion.html', job_id=id)


@app.route('/Insertion_data', methods=["GET", "POST"])
def getData():
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    num = request.form["phone"]
    job = request.form["job_id"]
    date = request.form["date"]
    print(request.form)
    Name = fname + " " + lname
    return render_template('data.html', name=Name, Email=email, Number=num, JOB=job, Date=date)

@app.route('/Insert_jobs', methods=["GET", "POST"])
def getjobsData():
    id = request.form["id"]
    title = request.form["title"]
    min = request.form["min"]
    max = request.form["max"]
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    cur.execute("INSERT INTO HR.JOBS(JOB_ID, JOB_TITLE, MIN_SALARY, MAX_SALARY) VALUES (:0, :1, :2,:3)", 
                (id, title,  int(min), int(max)))
    con.commit()
    cur.close()
    con.close()
    return render_template('after_submit.html')

@app.route('/empty_View')
def empty():
    return render_template('empty.html')

@app.route('/insert_jobs_View')
def jobs_view():
    return render_template('Insert_jobs.html')

@app.route('/login_View')
def login():
    return render_template('login.html')


@app.route("/submit_form", methods=["GET", "POST"])
def submit_form():
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    Id = request.form["id"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    login_id = request.form["loginid"]
    usertype_id = request.form["usertype_id"]
    ispending = request.form["ispending"]
    isapproved = request.form["isapproved"]
    print(("SQL STATEMENT:     INSERT INTO IPMS.USERS VALUES({}, '{}', '{}', {},{},{},{}, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)").format(int(Id), lname, fname, login_id, usertype_id, int(ispending), int(isapproved)))
    # Insert the data into the database
    cur.execute(("INSERT INTO IPMS.USERS VALUES({}, '{}', '{}', {},{},{},{}, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)").format(int(Id), lname, fname, login_id, usertype_id, int(ispending), int(isapproved)))
    con.commit()
    cur.close()
    con.close()
    return render_template('after_submit.html')


    # if request.method == "POST":
    #     print("Posting")
    #     connection = oracledb.connect(
    #         user=user, password=password, dsn=conn_string)
    #     cur = connection.cursor()
    #     cur.execute('INSERT INTO IPMS.USERS VALUES({user_id}, {last_name}, {first_name}, {login_id}, {usertype_id}, {is_pending}, {is_approved}, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)', user_id = 4, last_name = "Collison", first_name = "Juanita", login_id = 1, usertype_id = 1, is_pending = true, is_approved = false)
    #     cur.close()
    #     connection.close()
    
    # # Pass the data to the template to display in the HTML table
    # return render_template('index.html', data=data, job_id=id)


if __name__ == '__main__':
    app.run()
