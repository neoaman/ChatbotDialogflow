try:
    import urllib
    import json
    import os
    from flask import Flask,request,make_response,render_template,redirect,session
    import processing as ps
    import datetime
    from flask_sqlalchemy import SQLAlchemy
    # from datetime import datetime
except Exception as e:
    print("Module not found {}".format(e))


app = Flask(__name__)
with open("config.json") as c:
    params = json.load(c)["params"]
app.config['SQLALCHEMY_DATABASE_URI'] = params['neomi_uri']
app.secret_key = 'super-secret-key'

db = SQLAlchemy(app)
class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40),nullable=False)
    course = db.Column(db.String(40),nullable=False)
    branch = db.Column(db.String(40),nullable=False)
    phone_num = db.Column(db.String(13),nullable=False)
    date = db.Column(db.String(12),nullable=True)
    email = db.Column(db.String(20),nullable=False)


@app.route('/')
def home():

    return render_template('aman.html')

@app.route('/webhook', methods=['POST'])
def webhook():

    if request.method == "POST":
        req = request.get_json(silent=True,force=True)
        # This req will get the json output of the chatbot everyting
        # res will process the data 
        res = processRequest(req)
        res = json.dumps(res,indent=4)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r

def processRequest(req):
    # Get all queryResult
    query_response = req['queryResult']
    # text = query_response.get('queryText',None)
    # parameters = query_response.get('parameters',None)
    # print(query_response.get('action',None))

    if query_response.get('action',None) == 'input.appointment':
        
        if query_response.get('fulfillmentText',None) != None:
            print(query_response.get('fulfillmentText',None))
            return query_response.get('fulfillmentText',None)
        else:
            parameters = query_response.get('parameters',None)
            print()
            keys = ['geo-city','course','date','mobile','email']
            values = list(map(parameters.get, keys))
            """ Add to the database"""

            values,speech=ps.appointmentset2(values)

            name = 'Unknown'
            course = values[1]
            branch = values[0]
            date = str(values[2])[:10]
            phone_num = values[3]
            email = values[4]
            entry = Contacts(name =name,course = course, branch = branch, phone_num = phone_num, email=email ,date=date )
            db.session.add(entry)
            db.session.commit()
            print(speech)
            print('success')
            """ Added to database"""
            return speech
    else:
        print('not yet')
    
    if query_response.get('action',None) == 'input.duration':
        if query_response.get('fulfillmentText',None) != None:
            print(query_response.get('fulfillmentText',None))
            return query_response.get('fulfillmentText',None)
        else:
            parameters = query_response.get('parameters',None)
            keys = ['course']
            values = list(map(parameters.get, keys))
            return ps.courseduration(*values)

@app.route("/admin",methods=['GET','POST'])
def adminpage():
     
    if ('user' in session and session['user'] == params['admin_user']):
        if request.method =='POST':
            branch = request.form.get('branch')
            sdate = request.form.get('startdate')
            edate = request.form.get('enddate')
            if sdate == "" and branch!='All':
                contactinfo = Contacts.query.filter_by(branch=branch).all()
            elif sdate !="" and edate !="" and branch =='All':
                contactinfo = Contacts.query.filter(Contacts.date.between(sdate,edate)).filter_by().all()
            elif sdate =="" and edate =="" and branch =='All':
                contactinfo = Contacts.query.filter_by().all()            
            else:
                contactinfo = Contacts.query.filter(Contacts.date.between(sdate,edate)).filter_by(branch=branch).all()
        else:
            contactinfo = Contacts.query.filter_by().all()
        return render_template('admin.html',info=contactinfo)
    else:
        return render_template('login.html')
    
@app.route("/delete/<int:sno>")
def delete(sno):
    del_post= Contacts.query.filter_by(sno=sno).first()
    db.session.delete(del_post)
    db.session.commit()
    return redirect("/admin")

@app.route("/login",methods=['GET','POST'])
def logIn():
    if ('user' in session and session['user'] == params['admin_user']):
        contactinfo = Contacts.query.filter_by(branch='Bengaluru').all()
        return render_template('admin.html',info=contactinfo)
    if request.method =='POST':
        passs  = request.form.get('password')
        uname = request.form.get('loginid')
        if (uname == params['admin_user'] and passs == params['admin_pass']) :
            session['user'] = uname
            contactinfo = Contacts.query.filter_by(branch='Bengaluru').all()
            return render_template('admin.html',info=contactinfo)
        else:

            return render_template('login.html', warn = "Wrong Id or Password")
        # Redirect to admin
    return render_template('login.html',params=params)

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/')

app.run(debug=True)