import mysql.connector
import xlrd
import os
from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
from datetime import datetime


app = Flask(__name__)

hostname = 'localhost'
username = 'admin'
password = 'Password@123'
database = 'tcdata'



ALLOWED_EXTENSIONS = set(['csv', 'xls', 'xlsx'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# def initDb():
#     global myConnection
#     myConnection = mysql.connector.connect(host='TCTINFRA', user='admin', passwd='Password@123', db='tcdata')

@app.route("/view", methods=['GET', 'POST'])
def view():
    try:
        # initDb()
        db = mysql.connector.connect(host='localhost', user='rahul', passwd='Password@123', db='tcdata')
        #cur = db.cursor()

        # conn = MongoClient('mongodb://admin:admin123@TCTINFRA:27017')
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    db = mysql.connector.connect(host='localhost', user='rahul', passwd='Password@123', db='tcdata')
    cur = db.cursor()
    cur.execute("SELECT testcategory, testname, testsuite, testscript, testdescription, no_of_tests, centos, ubuntu1604, ubuntu1804, sanity, regression, performance, releases, fullcycle, automationstatus, automationtype, canbeMgpu, isMgpu, execution_time_in_min, coverageDate FROM tctestdata;")
    collection=cur.fetchall()
    # db = conn.tcdata
    # collection = db.tctestdata.find()
    # for x in collection.find():
    #   print(x)
    return render_template("view.html",data=collection)

@app.route("/bkcview", methods=['GET', 'POST'])
def bkcview():
    try:
        db = mysql.connector.connect(host='localhost', user='rahul', passwd='Password@123', db='tcdata')
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    db = mysql.connector.connect(host='localhost', user='rahul', passwd='Password@123', db='tcdata')
    cur = db.cursor()
    cur.execute("SELECT bkcdate, bkcversion FROM tcbkcdata ORDER BY bkcdate ASC;")
    collection=cur.fetchall()
    return render_template("bkc.html",data=collection)

@app.route('/delete', methods = ['POST', 'GET'])
def delete():
    if request.method == 'POST':
        tstname= request.form['testname']
        try:
            # initDb()
            # db = MySQLdb.connect(host='localhost', user='admin', passwd='Password@123', db='tcdata', port='3309')
            db = mysql.connector.connect(host='localhost', user='rahul', passwd='Password@123', db='tcdata')
            print("Connected successfully!!!")
        except:
            print("Could not connect to mysql")
        sql_Delete_query = "DELETE FROM tctestdata WHERE testname = %s"
        #testname = tstname
        db = mysql.connector.connect(host='localhost', user='rahul', passwd='Password@123', db='tcdata')


        adr = (request.form['testname'], )

        #mycursor.execute(sql, adr)

        cursor = db.cursor()
        cursor.execute(sql_Delete_query, adr)
        db.commit()
        val="record deleted successfully"
        return render_template('delete.html', key=val)
    else:
        return render_template('delete.html')



@app.route("/templateview", methods=['GET', 'POST'])
def templateview():
    # if request.method == 'GET':
        try:
            db = mysql.connector.connect(host='localhost', user='rahul', passwd='Password@123', db='tcdata')
            print("Connected successfully!!!")
        except:
            print("Could not connect to MongoDB")

        # db = mysql.connector.connect(host='localhost', user='rahul', passwd='Password@123', db='tcdata')
        cur = db.cursor()
        query="SELECT bkcversion FROM tcbkcdata ORDER by bkcdate DESC LIMIT 1;"
        cur.execute(query)
        current=cur.fetchone()
        crntvalue=current[0]
        #crntvalue=val[0]
        query="SELECT bkcversion FROM tcbkcdata ORDER by bkcdate DESC LIMIT 1,1;"
        cur.execute(query)
        previous=cur.fetchone()
        prvsvalue=previous[0]
        cur.execute("SELECT bkcdate FROM tcbkcdata ORDER by bkcdate DESC LIMIT 1;")
        currentDate=cur.fetchone()
        crntDate=currentDate[0]
        cur.execute("SELECT bkcdate FROM tcbkcdata ORDER by bkcdate DESC LIMIT 1,1;")
        previousDate=cur.fetchone()
        prvsDate=previousDate[0]
        return render_template("template.html", crnt=crntvalue, prvs=prvsvalue, crntdate=crntDate, prvsdate=prvsDate)
    # else:
        # return render_template('template.html')

@app.route('/bkcadd', methods = ['POST', 'GET'])
def bkcadd():
    if request.method == 'POST':

        bkcdate = request.form['date']
        bkcversion = request.form['BKC_Version']

        try:

            db = mysql.connector.connect(host='localhost', user='rahul', passwd='Password@123', db='tcdata')

            print("Connected successfully!!!")
        except:
            print("Could not connect to mysql")

        sql_insert_query = """ INSERT INTO tcbkcdata ( bkcdate, bkcversion) VALUES(%s, %s);"""
        sql_insert_tuple = (bkcdate, bkcversion)
        db = mysql.connector.connect(host='localhost', user='rahul', passwd='Password@123', db='tcdata')
        cursor = db.cursor()
        result  = cursor.execute(sql_insert_query, sql_insert_tuple)
        db.commit()
        #########
        #cursor = db.cursor()
        cursor.execute("SELECT bkcdate, bkcversion FROM tcbkcdata;")
        collection=cursor.fetchall()


        val="data added successfully"
        return render_template('bkc.html',key=val, data=collection)
    else:
        return render_template('bkc.html')

@app.route('/exceladd', methods = ['POST', 'GET'])
def exceladd():
    if request.method == 'POST':
        tstcategory=request.form['testcategory']
        tstname= request.form['testname']
        tstsuite= request.form['testsuite']
        tstscript= request.form['testscript']
        tstdescription= request.form['description']
        tstnooftests= request.form['no.of.tests']
        automationStatus = request.form["AutomationStatus"]
        automationType = request.form["AutomationType"]
        canBeMGPU = request.form["CanBeMGPU"]
        isMGPU = request.form["IsMGPU"]

        now = datetime.now()
        formatted_date = now.strftime('%d-%m-%y:%H:%M:%S')

        try:
            # initDb()
            # db = MySQLdb.connect(host='localhost', user='admin', passwd='Password@123', db='tcdata', port='3309')
            db = mysql.connector.connect(host='localhost', user='rahul', passwd='Password@123', db='tcdata')

            print("Connected successfully!!!")
        except:
            print("Could not connect to mysql")

        sql_insert_query = """ INSERT INTO tctestdata (testcategory, testname, testsuite, testscript, testdescription, no_of_tests, centos, ubuntu1604, ubuntu1804, sanity, regression, performance, releases, fullcycle, automationstatus, automationtype, canbeMgpu, isMgpu, execution_time_in_min, coverageDate)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        #sql_insert_tuple = ('3', tstcategory, tstname, tstscript, tstnooftests, 'centos', 'ubuntu16', 'ubuntu18', 'yes', 'no', '2', formatted_date)
        sql_insert_tuple = (tstcategory, tstname, tstsuite, tstscript, tstdescription, tstnooftests, 'yes', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'yes', automationStatus, automationType, canBeMGPU, isMGPU, '1', formatted_date)
        db = mysql.connector.connect(host='localhost', user='rahul', passwd='Password@123', db='tcdata')
        cursor = db.cursor()
        result  = cursor.execute(sql_insert_query, sql_insert_tuple)
        db.commit()
        # myConnection.commit()
        print ("Record inserted successfully into python_users table")
        val="Test added successfully"


        # return render_template({'key_val':val})
        #return val
        return render_template('add.html', key=val)
    else:
        return render_template('add.html')

# @app.route('/add', methods = ['POST', 'GET'])
# def add():
#     if request.method == 'POST':
#         f = request.files['xlfile']
#         f.save(secure_filename(f.filename))
#         return 'file uploaded successfully'
#
#     else:
#         return render_template('add.html')

@app.route('/add', methods = ['POST', 'GET'])
def add():
    if request.method == 'POST':

        app.config['UPLOAD_FOLDER'] = '/home/automation/TCapp/excel/'

        f = request.files['xlfile']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))

        now = datetime.now()
        formatted_date = now.strftime('%d-%m-%y:%H:%M:%S')

        # sheet = request.form['xlfile']
        # data = pd.read_excel(f)

        book = xlrd.open_workbook('/home/automation/TCapp/excel/excel.xlsx')
        sheet = book.sheet_by_name('Sheet1')


        #db = mysql.connector.connect(host='localhost', user='rahul', passwd='Password@123', db='tcdata')
        #cursor = db.cursor()
        sql_insert_query = """ INSERT INTO tctestdata (testcategory, testname, testsuite, testscript, testdescription, no_of_tests, centos, ubuntu1604, ubuntu1804, sanity, regression, performance, releases, fullcycle, automationstatus, automationtype, canbeMgpu, isMgpu, execution_time_in_min, coverageDate)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

        for r in range(1, sheet.nrows):
            tstcategory = sheet.row(r)[0].value
            tstname = sheet.row(r)[1].value
            tstsuite = sheet.row(r)[2].value
            tstscript = sheet.row(r)[3].value
            tstdescription = sheet.row(r)[4].value
            no_of_tests = sheet.row(r)[5].value
            centos = sheet.row(r)[6].value
            ubuntu1604 = sheet.row(r)[7].value
            ubuntu1804 = sheet.row(r)[8].value
            sanity = sheet.row(r)[9].value
            regression = sheet.row(r)[10].value
            performance = sheet.row(r)[11].value
            releases = sheet.row(r)[12].value
            fullcycle = sheet.row(r)[13].value
            automationstatus = sheet.row(r)[14].value
            automationtype = sheet.row(r)[15].value
            canbeMGPU = sheet.row(r)[16].value
            isMGPU = sheet.row(r)[17].value
            executiontime = sheet.row(r)[18].value


            # Assign values from each row
            sql_insert_tuple = (tstcategory, tstname, tstsuite, tstscript, tstdescription, no_of_tests, centos, ubuntu1604, ubuntu1804, sanity, regression, performance, releases, fullcycle, automationstatus, automationtype, canbeMGPU, isMGPU, executiontime, formatted_date)

            db = mysql.connector.connect(host='localhost', user='rahul', passwd='Password@123', db='tcdata')
            cursor = db.cursor()

            cursor.execute(sql_insert_query, sql_insert_tuple)

            db.commit()

            # Close the cursor


            # Close the database connection
            # db.close()

        # print ("Record inserted successfully into python_users table")
        val="File inserted successfully"
        return render_template('add.html', key=val)

    else:
        return render_template('add.html')

@app.route('/', methods = ['POST', 'GET'])
def main():
    db = mysql.connector.connect(host='localhost', user='rahul', passwd='Password@123', db='tcdata')

    cur = db.cursor()
    query="SELECT bkcversion FROM tcbkcdata ORDER by bkcdate DESC LIMIT 1;"
    cur.execute(query)
    current=cur.fetchone()
    crntvalue=current[0]
    #crntvalue=val[0]
    query="SELECT bkcversion FROM tcbkcdata ORDER by bkcdate DESC LIMIT 1,1;"
    cur.execute(query)
    previous=cur.fetchone()
    prvsvalue=previous[0]
    cur.execute("SELECT bkcdate FROM tcbkcdata ORDER by bkcdate DESC LIMIT 1;")
    currentDate=cur.fetchone()
    crntDate=currentDate[0]
    cur.execute("SELECT bkcdate FROM tcbkcdata ORDER by bkcdate DESC LIMIT 1,1;")
    previousDate=cur.fetchone()
    prvsDate=previousDate[0]
    return render_template("template.html", crnt=crntvalue, prvs=prvsvalue, crntdate=crntDate, prvsdate=prvsDate)

@app.route("/perfview", methods=['GET', 'POST'])
def view():

    return render_template("perf.html")


if __name__ == "__main__":
    app.run(host="10.130.163.64",port=8000, debug=True)
