from flask import (Flask, render_template, redirect, url_for, 
                   request)
import requests
import extractlcc
import json
import re
import ast

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("landing.html", displaydata={}, errordata=0)

@app.route('/submit', methods=['POST'])
def submit():
    # validate length and characters in query
    if len(request.form['query']) > 200:
        return render_template("viz.html", displaydata={}, errordata=4)
    elif re.compile(r'[^ a-zA-Z]').search(request.form['query']):
        return render_template("viz.html", displaydata={}, errordata=2)
    else:
        query = request.form['query']

    # validate dropdown menu
    choice = request.form['type']
    correct_choices = set(['lcc', 'date', 'topic'])
    if not choice in correct_choices:
        return render_template("viz.html", displaydata={}, errordata=3)

    # extract campus info from the form
    campus = ast.literal_eval(request.form['campus'])
    campus_code = list(campus)[0]
    campus_name = list(campus.values())[0]

    # make an api request using the inserting the query variable in the url
    resp = requests.get('http://onesearch.cuny.edu/PrimoWebServices/xservice/search/brief?&institution=%s&query=any,contains,%s&query=facet_rtype,exact,books&indx=1&lang=eng&json=true' % (campus_code, query))

    # assign the api data to a variable, pass it to the parsing function
    apicall = json.loads(resp.text)
    readydata = extractlcc.extract(apicall, choice)

    # if the parsing function fails, dispaly an error, else display viz.html with data
    if readydata == False:
        return render_template("viz.html", displaydata={}, errordata=1) 
    else:
        return render_template("viz.html", displaydata=readydata, errordata=0, val=query, campus=campus)

if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
