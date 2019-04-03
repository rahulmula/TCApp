import pymongo
from pymongo import MongoClient
from flask import Flask
from flask import request


# try:
#     conn = MongoClient('mongodb://admin:admin123@TCTINFRA:27017')
#     print("Connected successfully!!!")
# except:
#     print("Could not connect to MongoDB")
# db = conn.tcdata
# db.tctestdata.delete_one({"id": "2"})

# def get_tctestlist():
#     try:
#         conn = MongoClient('mongodb://admin:admin123@TCTINFRA:27017')
#         print("Connected successfully!!!")
#     except:
#         print("Could not connect to MongoDB")
#     db = conn.tcdata
#     collection = db.tctestdata.find()

try:
    conn = MongoClient('mongodb://admin:admin123@TCTINFRA:27017')
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

db = conn.tcdata
collection = db.tctestdata
tcCategory = request.form['testcategory']
emp_rec1={"uid":"4", "category":tcCategory, "testname":"KFDTest", "testscript":"KFDTest.sh", "no_of_tests":"0.1", "os_applicability": {
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
