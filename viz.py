from flask import (Flask, render_template, redirect, url_for, 
                   request)
import requests
import extractlcc
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("viz.html")


@app.route('/submit', methods=['POST'])
def submit():
	query = request.form['query']
	resp = requests.get('http://onesearch.cuny.edu/PrimoWebServices/xservice/search/brief?&institution=KB&onCampus=false&query=title,contains,{{ query }}&indx=1&lang=eng&json=true')
	apicall = json.loads(resp.text)
	readydata = extractlcc.extract(apicall)
	return redirect(url_for('index'))


app.run(debug=True, port=8000, host='0.0.0.0')
