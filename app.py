from flask import Flask,render_template,redirect,url_for,session,request

import pandas as pd
#import sheetTest as st


tups=tuple()
email='nwasifali7860@gmail.com'

app=Flask(__name__)

app.secret_key=hex(889923)

def filter_tuples_by_id(tuples, student_id):
    return [tup for tup in tuples if tup[0] == student_id]

@app.route('/',methods=["GET","POST"])
def index():
    if 'username'  in session.keys():
        return redirect(url_for('dashboard'))
    if request.method=="POST":
        
        if request.form["username"]=="admin" and request.form["pass"]=='admin':
            session["username"]="admin"
            return redirect(url_for('dashboard'))
    
        
    
    return render_template("index.html")

def read_sheet():
    df=pd.read_csv("https://docs.google.com/spreadsheets/d/1IDjfasHsR4IK3496i2CZSYInwZgYX-G6hufR5LHEl8Y/export?format=csv")


    records=df.to_dict(orient='records')
    tups=[tuple(record.values()) for record in records]
    print("Fetched Data from Google sheet Successfully")
    #print(records)
    return tups

@app.route('/dashboard',methods=["GET","POST"])
def dashboard():
    #if request.method=="GET":
    #sheet_id="1IDjfasHsR4IK3496i2CZSYInwZgYX-G6hufR5LHEl8Y"
    if 'username' not in session.keys():
        return redirect(url_for('index'))
    tups=read_sheet()
    
    return render_template("dashboard.html",records=tups)




@app.route("/search",methods=["GET","POST"])
def search():
    if 'username' not in session.keys():
        return redirect(url_for('index'))
    if request.method=='POST':
        id=request.form['id']
        records=read_sheet()
        clustered_results=filter_tuples_by_id(records,float(id))
        #print(clustered_results)
        if clustered_results:
            return render_template('search.html',result=clustered_results)
        else:
            return render_template('search.html', msg='Data not found')
    elif request.method=="GET":
        return render_template('search.html')
        
    return render_template("search.html")


@app.route("/logout")
def logout():
    if 'username' not in session.keys():
        return redirect(url_for('index'))
    session.clear()
    return redirect(url_for('index'))

if __name__=="__main__":
    app.run(debug=True)