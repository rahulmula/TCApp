import pymongo
import mysql.connector
import xlrd
from pymongo import MongoClient
from flask import Flask, render_template, request, url_for


app = Flask(__name__)

hostname = 'localhost'
username = 'admin'
password = 'Password@123'
database = 'tcdata'

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
    cur.execute("SELECT * FROM tctestdata;")
    collection=cur.fetchall()
    # db = conn.tcdata
    # collection = db.tctestdata.find()
    # for x in collection.find():
    #   print(x)
    return render_template("view.html",data=collection)


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
        return val
    else:
        return render_template('delete.html')


@app.route('/exceladd', methods = ['POST', 'GET'])
def exceladd():
    if request.method == 'POST':
        tstcategory=request.form['testcategory']
        tstname= request.form['testname']
        tstsuite= request.form['testsuite']
        tstscript= request.form['testscript']
        tstdescription= request.form['description']
        tstnooftests= request.form['no.of.tests']

        # Get data from fields
        form = request.form.getlist('check')

        if form.getvalue('centos'):
            centos = form.getvalue('centos')
        elif form.getvalue('ubuntu16'):
            ubuntu1604 = form.getvalue('ubuntu16')
        elif form.getvalue('ubuntu18'):
            ubuntu1804 = form.getvalue('ubuntu18')

        try:
            # initDb()
            # db = MySQLdb.connect(host='localhost', user='admin', passwd='Password@123', db='tcdata', port='3309')
            db = mysql.connector.connect(host='localhost', user='rahul', passwd='Password@123', db='tcdata')

            print("Connected successfully!!!")
        except:
            print("Could not connect to mysql")

        sql_insert_query = """ INSERT INTO tctestdata (uid, category ,testname, testscript, no_of_tests, fullcycle, automationstatus, automationtype, canbeMgpu, isMgpu, execution_time_in_min, coverageDate)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        sql_insert_tuple = ('3', tstcategory, tstname, tstscript, tstnooftests, centos, ubuntu16, ubuntu18, 'yes', 'no', '2', '2018-01-11')

        db = mysql.connector.connect(host='localhost', user='rahul', passwd='Password@123', db='tcdata')
        cursor = db.cursor()
        result  = cursor.execute(sql_insert_query, sql_insert_tuple)
        db.commit()
        # myConnection.commit()
        print ("Record inserted successfully into python_users table")
        val="Test added successfully"


        # return render_template({'key_val':val})
        return val
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

        sheet = request.form['xlfile']
        # data = pd.read_excel(f)

        book = xlrd.open_workbook(sheet)
        sht = book.sheet_by_index(0)

        db = mysql.connector.connect(host='localhost', user='rahul', passwd='Password@123', db='tcdata')
        cursor = db.cursor()
        sql_insert_query = """ INSERT INTO tctestdata (uid, category ,testname, testscript, no_of_tests, fullcycle, automationstatus, automationtype, canbeMgpu, isMgpu, execution_time_in_min, coverageDate)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

        for r in range(1, sheet.nrows):
            tstcategory = sheet.cell(r,1).value
            tstname = sheet.cell(r,2).value
            tstscript = sheet.cell(r,3).value
            tstnooftests = sheet.cell(r,4).value

            # Assign values from each row
            sql_insert_tuple = ('3', tstcategory, tstname, tstscript, tstnooftests,'yes', 'fullyautomated', 'e2e', 'yes', 'no', '2', '2018-01-11')
            result  = cursor.execute(sql_insert_query, sql_insert_tuple)

            # Close the cursor
            cursor.close()

            db.commit()

            # Close the database connection
            # db.close()

        print ("Record inserted successfully into python_users table")
        val="Test added successfully"
        return val

    else:
        return render_template('add.html')

        # Open the workbook and define the worksheet
    #     book = xlrd.open_workbook("pytest.xls")
    #     sheet = book.sheet_by_name("source")
    #
    #
    #     try:
    #         # initDb()
    #         # db = MySQLdb.connect(host='localhost', user='admin', passwd='Password@122', db='tcdata', port='3309')
    #         db = mysql.connector.connect(host='localhost', user='rahul', passwd='Password@123', db='tcdata')
    #         # cur = myConnection.cursor()
    #         # conn = MongoClient('mongodb://admin:admin123@TCTINFRA:27017')
    #         print("Connected successfully!!!")
    #     except:
    #         print("Could not connect to mysql")
    #
    #     for r in range(1, sheet.nrows):
    #
    #
    #     sql_insert_query = """ INSERT INTO tctestdata (uid, category ,testname, testscript, no_of_tests, fullcycle, automationstatus, automationtype, canbeMgpu, isMgpu, execution_time_in_min, coverageDate)
    #     VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    #     sql_insert_tuple = ('3', tstcategory, tstname, tstscript, tstnooftests,'yes', 'fullyautomated', 'e2e', 'yes', 'no', '2', '2018-01-11')
    #     # db = MySQLdb.connect(host='10.130.163.64', user='admin', passwd='Password@123', db='tcdata', port=3309)
    #     # db=connection.MySQLConnection(host='localhost', user='admin', passwd='Password@123', db='tcdata', port=3309)
    #     db = mysql.connector.connect(host='localhost', user='rahul', passwd='Password@123', db='tcdata')
    #     #cursor = myConnection.cursor()
    #     cursor = db.cursor()
    #     result  = cursor.execute(sql_insert_query, sql_insert_tuple)
    #     db.commit()
    #     # myConnection.commit()
    #     print ("Record inserted successfully into python_users table")
    #     val="Test added successfully"
    #     return val
    # else:
    #     return render_template('add.html')

@app.route('/', methods = ['POST', 'GET'])
def main():
    return render_template("template.html")

if __name__ == "__main__":
    app.run(host="10.130.163.64",port=8000)
