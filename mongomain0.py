import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/view", methods=['GET', 'POST'])
def view():
    try:
        conn = MongoClient('mongodb://admin:admin123@TCTINFRA:27017')
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
            conn = MongoClient('mongodb://admin:admin123@TCTINFRA:27017')
            print("Connected successfully!!!")
        except:
            print("Could not connect to MongoDB")
            # conn = MongoClient('mongodb://admin:admin123@TCTINFRA:27017')
        db = conn.tcdata
        collection = db.tctestdata
        # tcCategory = request.form['testcategory']
        emp_rec1={"uid":"11", "category":tstcategory, "testname":tstname, "testscript":tstscript, "no_of_tests":tstnooftests, "os_applicability": {
                "centOS":"Yes",
                "ubuntu1604":"Yes",
                "ubuntu1804":"Yes"
                },
                "applicable_category": {
                "sanity":"Yes",
                "regression":"Yes",
                "performance":"Yes",
                "release":"Yes"
                },
                "fullcycle":"Yes",
                "automation_status":"FullyAutomated",
                "automation_type": "skynetE2E",
                "CanbeMgpu":"0.1",
                "IsMgpu":"0.1",
                "execution_time_in_min": "1",
                "coverageDate":"0.1"
                }
        rec_id1 = collection.insert_one(emp_rec1)
        print("Record inserted in the collection", rec_id1)
        val="Test added successfully"
        # return render_template({'key_val':val})
        return val
    else:
        return render_template('add.html')


@app.route('/', methods = ['POST', 'GET'])
def main():
    return render_template("template.html")

if __name__ == "__main__":
    app.run()
