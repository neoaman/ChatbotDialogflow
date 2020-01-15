# ChatbotDialogflow
This is only the flask part, I haven't given any Information about the Dialog flow here. I wish Creating Intents and entities is already done. 
## Tools Used: Python, ngrok (for webhooking to the dialogflow locally)
## Packages Used : Flask, Flask-SQLAlchemy, Json.

## In this repository I have connected the intents to the MYSQL data base.

## Here I have make use of dialog flow to create your Own chatbot using python Flask for webhook and make use of data storing it in the MYSQL database using the local Uri

### Given Below is the whle process for the webhook to get the json file from the Dialogflow and again store the information in the MYSQL server
``````
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
``````


## This Project is still going on so stay tuned.
