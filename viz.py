from flask import (Flask, render_template, redirect, url_for, 
                   request)
import requests
import extractlcc
import json
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("viz.html", displaydata={}, errordata=0)

@app.route('/submit', methods=['POST'])
def submit():
    # use regex to validate user input
    def checkstr(userinput, search=re.compile(r'[^ a-zA-Z]').search):
        return not bool (search(userinput))

    # get data from form in viz.html and check using checkstr()
    if checkstr(request.form['query']) == True:
        query = request.form['query']
    else:
        return render_template("viz.html", displaydata={}, errordata=2)

    choice = request.form['type']
    correct_choices = set(['lcc', 'date', 'genr'])
    if not choice in correct_choices:
        return render_template("viz.html", displaydata={}, errordata=3)
    else:
        pass

    # make an api request using the inserting the query variable in the url
    resp = requests.get('http://onesearch.cuny.edu/PrimoWebServices/xservice/search/brief?&institution=KB&onCampus=false&query=any,contains,%s&query=facet_rtype,exact,books&indx=1&lang=eng&json=true' % query)
	
    # assign the api data to a variable, pass it to the parsing function
    apicall = json.loads(resp.text)
    readydata = extractlcc.extract(apicall, choice)

    # if the parsing function fails, dispaly an error, else display viz.html with data
    if readydata == False:
        return render_template("viz.html", displaydata={}, errordata=1) 
    else:
        return render_template("viz.html", displaydata=readydata, errordata=0)

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='127.0.0.1')
