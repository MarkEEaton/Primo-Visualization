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

	# get data from form in viz.html
	choice = request.form['type'] 
	query = request.form['query']
	
	# make an api request using the inserting the query variable in the url
	resp = requests.get('http://onesearch.cuny.edu/PrimoWebServices/xservice/search/brief?&institution=KB&onCampus=false&query=any,contains,%s&indx=1&lang=eng&json=true' % query)
	
	# assign the api data to a variable, pass it to the parsing function
	apicall = json.loads(resp.text)
	readydata = extractlcc.extract(apicall, choice)

	# if the parsing function fails, dispaly an error, else display viz.html with data binded
	if readydata == False:
		return redirect('/error')
	else:
		return render_template("viz.html", displaydata=readydata)

@app.route('/error')
def handleerror():
	return render_template("error.html")

if __name__ == '__main__':
	app.run(debug=True, port=8000, host='0.0.0.0')
