# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 21:14:05 2017

@author: Ramakant
"""
import json, os
import shutil
from distutils.dir_util import copy_tree
#import shutil
from flask import Flask, render_template, request, redirect, session, abort
app = Flask(__name__)

# =============================================================================
# cur = mysql.connection.cursor()
# cur.execute("select * from cropeddata")
# 
# row = cur.fetchone()
# 
# if(row):
#     print(row[0])
# =============================================================================

@app.route("/")
def main():
    return "Welcome"

@app.route("/Authenticate")
def Authenticate():
#    cursor = mysql.connect().cursor()
#    cursor.execute("SELECT * from cropeddata")
#    data = cursor.fetchone()
    import pyodbc 
    server = 'RAMAKANT-HP' 
    database = 'opencv' 
    username = 'RAMAKANT-HP\RAMAKANT' 
    password = 'ramakant' 
    #cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cnxn = pyodbc.connect(driver='{SQL Server Native Client 11.0}', 
                      host=server, database=database, trusted_connection='yes',
                      user=username, password=password)
    cursor = cnxn.cursor()
    query="select * from cropeddata"
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = cursor.description
    result = [{columns[index][0]:column for index, column in enumerate(value)}   for value in rows]
    #new_str = string.replace(result, 'C:/Users/Ramakant/AnacondaProjects/opencvocr/outputdata', 'static')
    temp = json.dumps(result)
    x = temp.replace('C:/Users/Ramakant/AnacondaProjects/opencvocr/outputdata', 'static')
    final_result = json.loads(x)
    #json_result = json.dumps(result)
    
    data = [{
            "Name":"Ramakant",
            "Name1":"Kushwaha",
            "Name2":"rk"
            },
            {
            "Name":"Ramakant",
            "Name1":"Kushwaha",
            "Name2":"rk"
            }]
    #print(json_result)
    if rows is None:
        print("Username or Password is wrong")
    else:  
        print("Logged in successfully")
    
    return render_template(
        'index.html',**locals())

try:
#    path = 'C:/Users/Ramakant/AnacondaProjects/opencvocr/WebApp/static/'
#    for the_file in os.listdir(path):
#        file_path = os.path.join(path, the_file)
#        if os.path.isdir(file_path):
#            shutil.rmtree(file_path)
    path = "C:/Users/Ramakant/AnacondaProjects/opencvocr/WebApp/"
    for dir in os.listdir(path):
        if(dir == "static"):
            shutil.rmtree(os.path.join(path, dir))
            
    shutil.copytree("C:/Users/Ramakant/AnacondaProjects/opencvocr/outputdata/","C:/Users/Ramakant/AnacondaProjects/opencvocr/WebApp/static/")
#    copy_tree("C:/Users/Ramakant/AnacondaProjects/opencvocr/outputdata/","C:/Users/Ramakant/AnacondaProjects/opencvocr/WebApp/static/")

except :
    print("error in copy images")
    
if __name__ == "__main__":
    app.run()
