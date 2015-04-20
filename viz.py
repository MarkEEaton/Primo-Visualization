from flask import (Flask, render_template, redirect, url_for, 
                   request)
import requests
import extractlcc
import json
import pdb
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("viz.html", displaydata={})


@app.route('/submit', methods=['POST'])
def submit():
    # use regex to validate user input
    def checkstr(userinput, search=re.compile(r'[^ a-zA-Z]').search):
        return not bool (search(userinput))

    # get data from form in viz.html and check using checkstr()
    if checkstr(request.form['query']) == True:
        query = request.form['query']
        print 'checkstr is True'
    else:
        print 'checkstr is False'
        return redirect('/error2')
    choice = request.form['type']
	
    # make an api request using the inserting the query variable in the url
    resp = requests.get('http://onesearch.cuny.edu/PrimoWebServices/xservice/search/brief?&institution=KB&onCampus=false&query=any,contains,%s&query=facet_rtype,exact,books&indx=1&lang=eng&json=true' % query)
	
    # assign the api data to a variable, pass it to the parsing function
    apicall = json.loads(resp.text)
    readydata = extractlcc.extract(apicall, choice)

    # if the parsing function fails, dispaly an error, else display viz.html with data
    if readydata == False:
        return redirect('/error1')
    else:
        return render_template("viz.html", displaydata=readydata)

@app.route('/error1')
def handleerror1():
    return render_template("error1.html")

@app.route('/error2')
def handlerror2():
    return render_template("error2.html")

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
