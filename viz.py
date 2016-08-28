from flask import (Flask, render_template, request, session)
from wtforms import *
import requests
import extractfromjson
import json
import re
import ast

app = Flask(__name__)


facetchoices = [('lcc', 'Library of Congress Classification'), 
                ('creationdate', 'Creation Date'),
                ('topic', 'Topic')]
campuschoices = [('BB', 'Baruch'),
                 ('BM', 'BMCC'),
                 ('BX', 'Bronx CC'),
                 ('BC', 'Brooklyn College'),
                 ('CC', 'City College'),
                 ('SI', 'CSI'),
                 ('GC', 'Graduate Center'),
                 ('GJ', 'School of Journalism'),
                 ('CL', 'School of Law'),
                 ('NC', 'Guttman'),
                 ('HO', 'Hostos'),
                 ('HC', 'Hunter'),
                 ('JJ', 'John Jay'),
                 ('KB', 'Kingsborough'),
                 ('LG', 'LaGuardia'),
                 ('LE', 'Lehman'),
                 ('ME', 'Medgar Evers'),
                 ('NY', 'City Tech'),
                 ('QC', 'Queens College'),
                 ('QB', 'Queensborough'),
                 ('YC', 'York')
                 ]

# set up wtforms class
class SearchForm(Form):
    keywords = StringField('query', [
               validators.Length(max=200, message="length"), 
               validators.Regexp('^[ a-zA-Z]*$', message="regex")])
    campus = SelectField('Campus', choices=campuschoices,
             validators=[validators.Required(message="campus")])
    facet = SelectField('Facet', choices=facetchoices,
            validators=[validators.Required(message="facet")])


@app.route('/')
def index():
    form = SearchForm()
    return render_template("landing.html", displaydata={}, errordata=0, form=form)


@app.route('/submit', methods=['POST'])
def submit():
    form = SearchForm(request.form)
        
    def validateform(form):
        """ validates the form, else returns error codes """
        if form.campus and form.campus.data == "None":
            del form.campus
        if request.method == 'POST' and form.validate():
            global query
            query = form.keywords.data 
            return 
        else:
            print form.errors.itervalues().next()
            return form.errors.itervalues().next()
     
    def allvalidate():
        """ runs the validation; renders templates if validation fails """
        if validateform(form) == None:
            return False
        elif "length" in validateform(form):
            return render_template("viz.html", displaydata={},
                                   errordata=4, campus=chosencampusname)
        elif "regex" in  validateform(form):
            return render_template("viz.html", displaydata={},
                                   errordata=2, campus=chosencampusname)
        elif ("facet" or "campus") in validateform(form):
            return render_template("viz.html", displaydata={},
                                   errordata=3, campus=chosencampusname)
        else:
            return False 
    
    def managesession():
        global campus_code, chosencampusname
        if form.campus.data == "None":
            campus_code = session['campus_code']
            chosencampusname = session['chosencampusname']
            pass
        else: 
            campus_code = form.campus.data
            chosencampusname = dict(campuschoices).get(form.campus.data)
            session['campus_code'] = campus_code 
            session['chosencampusname'] = chosencampusname
            pass

    managesession()
    if allvalidate(): 
        return allvalidate()
    else: pass

    # make an api request using the inserting the query variable in the url
    resp = requests.get('http://onesearch.cuny.edu/PrimoWebServices'
                        '/xservice/search/brief?&institution={}&'
                        'query=any,contains,{}&query=facet_rtype,exact,'
                        'books&indx=1&loc=local,scope:(KB,AL,CUNY_BEPRESS)&'
                        'loc=adaptor,primo_central_multiple_fe'
                        '&json=true'.format(campus_code, query))

    # assign the api data to a variable, pass it to the parsing function
    apicall = json.loads(resp.text)
    readydata = extractfromjson.extract(apicall, form.facet.data)


    # if the parsing function fails, dispaly an error, else display
    # viz.html with data
    if readydata is False:
        return render_template("viz.html", displaydata={}, errordata=1,
                               campus=chosencampusname)
    else:
        return render_template("viz.html", displaydata=readydata,
                               errordata=0, val=query,
                               campus=chosencampusname)

app.secret_key = 'key goes here'

if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0', debug=True)
