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
login_id = cur.execute('select LOGIN_ID from IPMS.LOGIN')
for row in login_id:
    id.append(row[0])
cur.close()
connection.close()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/user_View', methods=['GET', 'POST'])
def get_data():
    print("Getting")
    connection = oracledb.connect(
        user=user, password=password, dsn=conn_string)
    cur = connection.cursor()
    cur.execute('select * from IPMS.USERS')
    data.clear()
    for row in cur:
        data.append({"ID": row[0], "First_Name": row[2], "Last_Name": row[1],
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
    cur.execute("SELECT P.PLACEMENT_ID, P.TITLE, P.DESCRIPTION, P.SKILLS, P.COMPANY_ID, C.COMPANY_NAME, C.ADDRESS, C.EMAIL, C.TELEPHONE, P.USER_ID, P.STATUS_ID FROM IPMS.PLACEMENTS P INNER JOIN IPMS.COMPANIES C ON P.COMPANY_ID = C.COMPANY_ID INNER JOIN IPMS.STATUS S ON P.STATUS_ID = S.STATUS_ID WHERE S.STATUS_TYPE = 'open'")
    
    for row in cur:
        jobs.append({"PID": row[0], "PTitle": row[1],
                    "Skills": row[3], "Desc": row[2], "Company_Name":row[5],
                    "Address": row[6], "Email": row[7],
                    "Tel": row[8], "UID":row[9], "SID":row[10]})


    # Close the cursor and connection
    cur.close()
    connection.close()
    # Pass the data to the template to display in the HTML table
    return render_template('placements.html', data=jobs)
    #return render_template('about.html')


@app.route('/about_View')
def about():
    return render_template('about.html')


# @app.route('/Insert_View')
# def insert():
#     return render_template('Insertion.html', job_id=id)


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

@app.route('/empty_View')
def empty():
    return render_template('empty.html')

@app.route('/View_Preferences_View')
def view_preferences():
    return render_template('ViewPreferences.html')

@app.route('/Students_View',methods=['GET'])
def Students():
    jobs = []
    connection = oracledb.connect(
        user=user, password=password, dsn=conn_string)
    cur = connection.cursor()
    cur.execute("SELECT U.USER_ID, U.FIRST_NAME, U.LAST_NAME, L.EMAIL, U.ISAPPROVED FROM IPMS.USERS U INNER JOIN IPMS.LOGIN L ON U.LOGIN_ID = L.LOGIN_ID WHERE USER_TYPE_ID=0")
    for row in cur:
        jobs.append({"UID": row[0], "UfName": row[1], "UlName": row[2], "Email": row[3], "App": row[4]})
    cur.close()
    connection.close()
    return render_template('Students.html', data=jobs)

@app.route('/choosePreference_View')
def choose_view():
    return render_template('choosePreference.html')

@app.route('/login_View')
def login():
    return render_template('login.html')

@app.route('/submit_login', methods=["GET", "POST"])
def submit_login():
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    cur.execute("SELECT max(LOGIN_ID) FROM IPMS.LOGIN")
    for row in cur:
        LId = row[0]
    cur.execute("SELECT max(USER_ID) FROM IPMS.USERS")
    for row in cur:
        UId = row[0]
    email = request.form["email"]
    pswd = request.form["pswd"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    usertype_id = 0
    ispending = 1
    isapproved = 0
    cur.execute(("INSERT INTO IPMS.LOGIN VALUES({}, '{}', '{}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)").format(int(LId)+1, email, pswd))
    cur.execute(("INSERT INTO IPMS.USERS VALUES({}, '{}', '{}', {},{},{},{}, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)").format(int(UId)+1, lname, fname, LId, usertype_id, int(ispending), int(isapproved)))
    con.commit()
    cur.close()
    con.close()
    return render_template('after_submit.html')


@app.route("/submit_form", methods=["GET", "POST"])
def submit_form():
    print("SUBMITTING")
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    Id = request.form["id"]
    usertype_id = request.form["usertype_id"]
    ispending = request.form["ispending"]
    isapproved = request.form["isaccepted"]
    print("TEST" + Id + usertype_id + ispending + isapproved)
    # Insert the data into the database
    print(("UPDATE IPMS.USERS SET USER_TYPE_ID = {}, ISPENDING = {}, ISAPPROVED = {}, UPDATED_AT = CURRENT_TIMESTAMP WHERE USER_ID = {}").format(usertype_id, ispending, isapproved, Id))
    cur.execute(("UPDATE IPMS.USERS SET USER_TYPE_ID = {}, ISPENDING = {}, ISAPPROVED = {}, UPDATED_AT = CURRENT_TIMESTAMP WHERE USER_ID = {}").format(usertype_id, ispending, isapproved, Id))
    con.commit()
    cur.close()
    con.close()
    return render_template('after_submit.html')

@app.route("/submit_placements_form", methods=["GET", "POST"])
def submit_pform():
    print("SUBMITTING")
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    Id = request.form["id"]
    user_id = request.form["userid"]
    status_id = request.form["statusid"]
    skills = request.form["skills"]
    desc = request.form["desc"]
    # Insert the data into the database
    print(("UPDATE IPMS.PLACEMENTS SET USER_ID = {}, SKILLS = '{}', DESCRIPTION = '{}', STATUS_ID = {}, UPDATED_AT = CURRENT_TIMESTAMP WHERE PLACEMENT_ID = {}").format(user_id, skills, desc, status_id, Id))
    cur.execute(("UPDATE IPMS.PLACEMENTS SET USER_ID = {}, SKILLS = '{}', DESCRIPTION = '{}', STATUS_ID = {}, UPDATED_AT = CURRENT_TIMESTAMP WHERE PLACEMENT_ID = {}").format(user_id, skills, desc, status_id, Id))
    con.commit()
    cur.close()
    con.close()
    return render_template('after_submit.html')


@app.route('/new_placement_view')
def view_new_placement():
    return render_template('new_placement.html')

@app.route('/new_placement', methods=["GET", "POST"])
def new_placement():
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    cur.execute("SELECT max(PLACEMENT_ID) FROM IPMS.PLACEMENTS")
    for row in cur:
        PId = row[0]
    #cur.execute("SELECT max(USER_ID) FROM IPMS.USERS")
    #for row in cur:
        #PId = row[0]
    title = request.form["title"]
    skills = request.form["skills"]
    desc = request.form["desc"]
    company_id = request.form["company_id"]
    
    if PId is None:
        PId = -1

    cur.execute(("INSERT INTO IPMS.PLACEMENTS VALUES({}, '{}', '{}', '{}', {}, 0, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)").format(int (PId)+1, title, skills, desc,company_id))
    #cur.execute(("INSERT INTO IPMS.USERS VALUES({}, '{}', '{}', {},{},{},{}, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)").format(int(UId)+1, lname, fname, LId, usertype_id, int(ispending), int(isapproved)))
    con.commit()
    cur.close()
    con.close()
    return render_template('new_placement.html')

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


@app.route('/delete_row/<int:id>', methods=['POST'])
def deleteRow(id):
    try:
        json = request.get_json()

        deleteFromID(json)

        return '0'

    except Exception as error:
        return str(error)

def deleteFromID(_row):
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    print("DELETE FROM IPMS.USERS WHERE USER_ID = "+_row)
    #cur.execute("DELETE FROM IPMS.USERS WHERE USER_ID = "+_row)
    con.commit()
    cur.close()
    con.close()
    return render_template('after_submit.html')




if __name__ == '__main__':
    app.run()
