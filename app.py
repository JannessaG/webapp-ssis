from flask import Flask,render_template,url_for,request,redirect,flash
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
app.secret_key = "secret"
#database connection
db = yaml.safe_load(open('dbconfig.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']


mysql = MySQL(app)
@app.route('/')
def students():
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM students");
	data = cur.fetchall()
	cur.close()
	return render_template('students.html',students=data)

@app.route('/courses')
def courses():
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM courses");
	data = cur.fetchall()
	cur.close()
	return render_template('course.html',courses=data)

@app.route('/colleges')
def colleges():
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM colleges");
	data = cur.fetchall()
	cur.close()
	return render_template('colleges.html',colleges=data)

# STDENTS -------------------------------------------------------------------
#INSERT DATA IN STUDENT TABLE
@app.route('/insert',methods=['POST'])
def insert():
	if request.method == "POST":
		flash("Data inserted successfully!")
		idEntry = request.form['idno']
		firstNameEntry = request.form['firstName']
		lastNameEntry = request.form['lastName']
		courseEntry = request.form['course']
		yearEntry = request.form['year']
		genderEntry = request.form['gender']
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO students(idno,firstName,lastName,course,year,gender) VALUES (%s,%s,%s,%s,%s,%s)",(idEntry,firstNameEntry,lastNameEntry,courseEntry,yearEntry,genderEntry));
		mysql.connection.commit()
		return redirect(url_for('students'))


#UPDATE DATA IN STUDENT TABLE
@app.route("/update",methods= ['POST','GET'])
def update():
	if request.method == 'POST':
		studno= request.form['no']
		idEntry = request.form['idno']
		firstNameEntry = request.form['firstName']
		lastNameEntry = request.form['lastName']
		courseEntry = request.form['course']
		yearEntry = request.form['year']
		genderEntry = request.form['gender']
		cur = mysql.connection.cursor()
		cur.execute("""UPDATE students SET idno=%s,firstName=%s,lastName=%s,course=%s,year=%s,gender=%s WHERE no=%s""",
			(idEntry,firstNameEntry,lastNameEntry,courseEntry,yearEntry,genderEntry,studno))
		flash("Data updated successfully!")
		mysql.connection.commit()
		return redirect(url_for('students'))

#DELETE TUPLE IN STUDENT DATA
@app.route("/delete/<string:idno>",methods=['POST','GET'])
def delete(idno):
	if len(idno)!=0:
		cur = mysql.connection.cursor()
		cur.execute("DELETE FROM students WHERE idno=%s",(idno,))
		mysql.connection.commit()
		cur.close()
		flash("Data deleted successfully!")
	return redirect(url_for('students'))

#SEARCH DATA
@app.route("/search",methods=['POST','GET'])
def search():
	if request.method=='POST':
		searchEntry = request.form['search']
		cur = mysql.connection.cursor()
		cur.execute("""SELECT * FROM students WHERE idno=%s or firstName=%s or lastName=%s or course=%s or year=%s  or gender=%s  """,
			(searchEntry,searchEntry,searchEntry,searchEntry,searchEntry,searchEntry));
		searchData = cur.fetchall()
		cur.close()
		return render_template('students.html',students=searchData)


#COURSES 
#---------------------------------------------------------------------------------
@app.route('/addcourse',methods=['POST','GET'])
def addcourse():
	if request.method == "POST":
		flash("Data inserted successfully!")
		CodeEntry = request.form['courseCode']
		CourseEntry = request.form ['courseName']
		collegeEntry = request.form ['courseCollege']
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO courses(courseCode,courseName,courseCollege) VALUES (%s,%s,%s)",(CodeEntry,CourseEntry,collegeEntry));
		mysql.connection.commit()
		return redirect(url_for('courses'))

@app.route("/courseUpdate",methods= ['POST'])
def courseUpdate():
	if request.method == 'POST':
		courseno = request.form['courseno']
		CodeEntry = request.form['courseCode']
		CourseEntry = request.form ['courseName']
		CollegeEntry = request.form ['courseCollege']
		cur = mysql.connection.cursor()
		cur.execute("""UPDATE courses SET courseCode=%s,courseName=%s,courseCollege=%s WHERE courseno=%s""",
			(CodeEntry,CourseEntry,CollegeEntry,courseno))
		flash("Data updated successfully!")
		mysql.connection.commit()
		return redirect(url_for('courses'))

@app.route("/coursedelete/<string:courseno>",methods=['POST','GET'])
def coursedelete(courseno):
	if len(courseno)!=0:
		cur = mysql.connection.cursor()
		cur.execute("DELETE FROM courses WHERE courseno=%s",(courseno,))
		mysql.connection.commit()
		cur.close()
		flash("Data deleted successfully!")
	return redirect(url_for('courses'))

@app.route("/courseSearch",methods=['POST','GET'])
def courseSearch():
	if request.method=='POST':
		searchEntry = request.form['search']
		cur = mysql.connection.cursor()
		cur.execute("""SELECT * FROM courses WHERE courseCode=%s or courseName=%s or courseCollege=%s  """,
			(searchEntry,searchEntry,searchEntry));
		searchData = cur.fetchall()
		cur.close()
		return render_template('course.html',courses=searchData)



#COLLEGE 
#-----------------------------------------------------------------------------------------------
@app.route('/addcollege',methods=['POST'])
def addcollege():
	if request.method == "POST":
		flash("Data inserted successfully!")
		collegeCodeEntry = request.form['collegeCode']
		collegeEntry = request.form ['collegeName']
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO colleges(collegeCode,collegeName) VALUES (%s,%s)",(collegeCodeEntry,collegeEntry));
		mysql.connection.commit()
		return redirect(url_for('colleges'))

@app.route("/collegeUpdate",methods= ['POST','GET'])
def collegeUpdate():
	if request.method == 'POST':
		collegeno = request.form['colno']
		collegecodeEntry = request.form['collegeCode']
		collegeEntry = request.form ['collegeName']
		cur = mysql.connection.cursor()
		cur.execute("""UPDATE colleges SET collegeCode=%s,collegeName=%s WHERE colno=%s""",
			(collegeEntry,collegecodeEntry,collegeno))
		flash("Data updated successfully!")
		mysql.connection.commit()
		return redirect(url_for('colleges'))

@app.route("/collegedelete/<string:colno>",methods=['POST','GET'])
def collegedelete(colno):
	if len(colno)!=0:
		cur = mysql.connection.cursor()
		cur.execute("DELETE FROM colleges WHERE colno=%s",(colno,))
		mysql.connection.commit()
		cur.close()
		flash("Data deleted successfully!")
	return redirect(url_for('colleges'))

@app.route("/collegeSearch",methods=['POST','GET'])
def collegeSearch():
	if request.method=='POST':
		searchEntry = request.form['search']
		cur = mysql.connection.cursor()
		cur.execute("""SELECT * FROM colleges WHERE collegeCode=%s or collegeName=%s""",
			(searchEntry,searchEntry));
		searchData = cur.fetchall()
		cur.close()
		return render_template('colleges.html',colleges=searchData)


#debug mode for development
if __name__ == "__main__":
	app.run(debug=True)
