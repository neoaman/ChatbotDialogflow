from datetime import datetime
import datetime as dt


def appointmentset(*args):
    week_days = ['Monday', 'Tuesday', 'Wednesday',
                 'Thursday', 'Friday', 'Saturday', 'Sunday']
    do = datetime.strptime(args[2][:10], '%Y-%m-%d')
    if week_days[do.weekday()] in ['Saturday', 'Sunday'] and args[0] in ['Bengaluru', 'Pune', 'Hydrabad', 'Mumbai']:
        speech = "actually {} is holiday so I am Shifting your Appointment to coming Monday at {} for {} course".format(week_days[do.weekday()], args[0], args[1])
    elif args[0] not in ['Bengaluru', 'Pune', 'Hydrabad', 'Mumbai'] and week_days[do.weekday()] not in ['Saturday', 'Sunday']:
        speech = "Sorry we have no branch at {} . So fixing your Appointment at Excelr Bangalore for {} Course on {}".format(args[0], args[1], args[2][:10])
    elif args[0] not in ['Bengaluru', 'Pune', 'Hydrabad', 'Mumbai'] and week_days[do.weekday()] in ['Saturday', 'Sunday']:
        speech = "Sorry we have no branch at {} . So fixing your Appointment at Excelr Bangalore for {} Course. Also {} is a holiday so we will meet on Upcoming Monday".format(args[0], args[1], args[2][:10])
    else:
        speech = 'fixing your Appointment at Excelr {} for {} Course on {}'.format(args[0], args[1], args[2][:10])
    return {
        "fulfillmentText": speech,
    }


def courseduration(course):
    duration = {'Data Science': '5 months', 'Data Analyst': '2 months',
                'Master in Data Science': '12 months'}

    speech = '{} course duration is about {}'.format(course, duration[course])
    return {
        "fulfillmentText": speech,
    }

def appointmentset2(args):

    """ For Date of Appointmnet_________________________ """
    week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    do = datetime.strptime(args[2][:10], '%Y-%m-%d')
    if week_days[do.weekday()] in ['Saturday', 'Sunday']:
        s1 = "I think {} is {} a holiday. ".format(args[2][:10],week_days[do.weekday()])
        if int(do.weekday()) == 6:
            args[2] = do+dt.timedelta(1)
        else:
            args[2] = do+dt.timedelta(2)
    else:
        s1 = ""
    
    """ For Location of Appointment_______________ """
    avilloc = ['Bengaluru', 'Pune', 'Hyderabad', 'Mumbai']
    if args[0] not in avilloc:
        s2 = "There is no ExcelR Branch at {} . ".format(args[0])
        args[0] = 'Bengaluru'
    else:
        s2 =""
    
    """ Final Post """
    speech = s1+s2+'So I am fixing your Appointment at Excelr {} for {} Course on {}'.format(args[0], args[1], str(args[2])[:10])
    
    return args,{
        "fulfillmentText": speech,
    }





