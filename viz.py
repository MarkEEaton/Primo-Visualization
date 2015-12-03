from flask import (Flask, render_template, request, session)
import requests
import extractfromjson
import json
import re
import ast

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("landing.html", displaydata={}, errordata=0)


@app.route('/submit', methods=['POST'])
def submit():
    # extract campus info from the form, otherwise extract from the session
    try:
        campus = ast.literal_eval(request.form['campus'])
    except:
        campus = session['campus']
        pass
    else:
        correct_campus = set(["{'BB': 'Baruch'}",
                              "{'BM': 'BMCC'}",
                              "{'BX': 'Bronx CC'}",
                              "{'BC': 'Brooklyn College'}",
                              "{'CC': 'City College'}",
                              "{'SI': 'CSI'}",
                              "{'GC': 'Graduate Center'}",
                              "{'GJ': 'School of Journalism'}",
                              "{'CL': 'School of Law'}",
                              "{'NC': 'Guttman'}",
                              "{'HO': 'Hostos'}",
                              "{'HC': 'Hunter'}",
                              "{'JJ': 'John Jay'}",
                              "{'KB': 'Kingsborough'}",
                              "{'LG': 'LaGuardia'}",
                              "{'LE': 'Lehman'}",
                              "{'ME': 'Medgar Evers'}",
                              "{'NY': 'City Tech'}",
                              "{'QC': 'Queens College'}",
                              "{'QB': 'Queensborough'}",
                              "{'YC': 'York'}"
                              ])
        if not request.form['campus'] in correct_campus:
            return render_template("viz.html", displaydata={},
                                   errordata=3, campus=campus)
        else:
            session['campus'] = ast.literal_eval(request.form['campus'])
    campus_code = list(campus)[0]

    # validate length and characters in query
    if len(request.form['query']) > 200:
        return render_template("viz.html", displaydata={},
                               errordata=4, campus=campus)
    elif re.compile(r'[^ a-zA-Z]').search(request.form['query']):
        return render_template("viz.html", displaydata={},
                               errordata=2, campus=campus)
    else:
        query = request.form['query']

    # validate dropdown menu
    choice = request.form['type']
    correct_choices = set(['lcc', 'creationdate', 'topic'])
    if choice not in correct_choices:
        return render_template("viz.html", displaydata={},
                               errordata=3, campus=campus)

    # make an api request using the inserting the query variable in the url
    resp = requests.get('http://onesearch.cuny.edu/PrimoWebServices'
                        '/xservice/search/brief?&institution={}&'
                        'query=any,contains,{}&query=facet_rtype,exact,'
                        'books&indx=1&loc=local,scope:(KB,AL,CUNY_BEPRESS)&'
                        'loc=adaptor,primo_central_multiple_fe'
                        '&json=true'.format(campus_code, query))

    # assign the api data to a variable, pass it to the parsing function
    apicall = json.loads(resp.text)
    readydata = extractfromjson.extract(apicall, choice)

    # if the parsing function fails, dispaly an error, else display
    # viz.html with data
    if readydata is False:
        return render_template("viz.html", displaydata={}, errordata=1,
                               campus=campus)
    else:
        return render_template("viz.html", displaydata=readydata,
                               errordata=0, val=query, campus=campus)

app.secret_key = 'key goes here'

if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
