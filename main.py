import pymongo
from mysql.connector import connection
import MySQLdb
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
        initDb()
        cur = myConnection.cursor()
        # conn = MongoClient('mongodb://admin:admin123@TCTINFRA:27017')
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")
    db = conn.tcdata
    collection = db.tctestdata.find()
    # for x in collection.find():
    #   print(x)
    return render_template("view.html",data=collection)

@app.route('/add', methods = ['POST', 'GET'])
def add():
    if request.method == 'POST':
        tstcategory=request.form['testcategory']
        tstname= request.form['testname']
        tstsuite= request.form['testsuite']
        tstscript= request.form['testscript']
        tstdescription= request.form['description']
        tstnooftests= request.form['no.of.tests']

        try:
            # initDb()
            db = MySQLdb.connect(host='localhost', user='admin', passwd='Password@123', db='tcdata', port='3309')
            # myConnection = mysql.connector.connect(host='10.130.163.64', user='admin', passwd='Password@123', db='tcdata', port='3309')
            # cur = myConnection.cursor()
            # conn = MongoClient('mongodb://admin:admin123@TCTINFRA:27017')
            print("Connected successfully!!!")
        except:
            print("Could not connect to mysql")

        sql_insert_query = """ INSERT INTO tctestdata (uid, category ,testname, testscript, no_of_tests, fullcycle, automationstatus, automationtype, canbeMgpu, isMgpu, execution_time_in_min, coverageDate)
        VALUES('2', tstcategory, tstname, tstsuite, tstscript, tstnooftests, 'fullyautomated', 'e2e', 'yes', 'no', '20', '2018-01-11');"""
        # db = MySQLdb.connect(host='10.130.163.64', user='admin', passwd='Password@123', db='tcdata', port=3309)
        db=connection.MySQLConnection(host='localhost', user='admin', passwd='Password@123', db='tcdata', port=3309)
        # myConnection = mysql.connector.connect(host='10.130.163.64', user='admin', passwd='Password@123', db='tcdata', port='3309')
        #cursor = myConnection.cursor()
        cursor = db.cursor()
        result  = cursor.execute(sql_insert_query)
        db.commit()
        # myConnection.commit()
        print ("Record inserted successfully into python_users table")
        val="Test added successfully"
        # db = conn.tcdata
        # collection = db.tctestdata
        # tcCategory = request.form['testcategory']
        # emp_rec1={"uid":"11", "category":tstcategory, "testname":tstname, "testscript":tstscript, "no_of_tests":tstnooftests, "os_applicability": {
        #         "centOS":"Yes",
        #         "ubuntu1604":"Yes",
        #         "ubuntu1804":"Yes"
        #         },
        #         "applicable_category": {
        #         "sanity":"Yes",
        #         "regression":"Yes",
        #         "performance":"Yes",
        #         "release":"Yes"
        #         },
        #         "fullcycle":"Yes",
        #         "automation_status":"FullyAutomated",
        #         "automation_type": "skynetE2E",
        #         "CanbeMgpu":"0.1",
        #         "IsMgpu":"0.1",
        #         "execution_time_in_min": "1",
        #         "coverageDate":"0.1"
        #         }
        # rec_id1 = collection.insert_one(emp_rec1)
        # print("Record inserted in the collection", rec_id1)

        # return render_template({'key_val':val})
        return val
    else:
        return render_template('add.html')


@app.route('/', methods = ['POST', 'GET'])
def main():
    return render_template("template.html")

if __name__ == "__main__":
    app.run()
