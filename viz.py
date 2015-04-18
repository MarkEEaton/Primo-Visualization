from flask import (Flask, render_template, redirect, url_for, 
                   request)
import requests
import extractlcc
import json
import pdb

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("viz.html", displaydata={})


@app.route('/submit', methods=['POST'])
def submit():
	choice = request.form['type'] 
	query = request.form['query']
	resp = requests.get('http://onesearch.cuny.edu/PrimoWebServices/xservice/search/brief?&institution=KB&onCampus=false&query=any,contains,%s&indx=1&lang=eng&json=true' % query)
	apicall = json.loads(resp.text)
	readydata = extractlcc.extract(apicall, choice)
	if readydata == False:
		return redirect('/error')
	else:
		return render_template("viz.html", displaydata=readydata)

@app.route('/error')
def handleerror():
	return render_template("error.html")

if __name__ == '__main__':
	app.run(debug=True, port=8000, host='0.0.0.0')
