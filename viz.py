from flask import (Flask, render_template, request, session)
from wtforms import *
import handlesubmit
import requests
import extractfromjson
import json
from key import key

app = Flask(__name__)


facetchoices = [('lcc', 'Library of Congress Classification'),
                ('creationdate', 'Creation Date'),
                ('topic', 'Topic')]
campuschoices = [('BB', 'Baruch'),
                 ('BM', 'BMCC'),
                 ('BX', 'Bronx CC'),
                 ('BC', 'Brooklyn College'),
                 ('CC', 'City College'),
                 ('NY', 'City Tech'),
                 ('SI', 'CSI'),
                 ('GC', 'Graduate Center'),
                 ('NC', 'Guttman'),
                 ('HO', 'Hostos'),
                 ('HC', 'Hunter'),
                 ('JJ', 'John Jay'),
                 ('KB', 'Kingsborough'),
                 ('LG', 'LaGuardia'),
                 ('LE', 'Lehman'),
                 ('ME', 'Medgar Evers'),
                 ('QC', 'Queens College'),
                 ('QB', 'Queensborough'),
                 ('GJ', 'School of Journalism'),
                 ('CL', 'School of Law'),
                 ('YC', 'York')
                 ]


class SearchForm(Form):
    """ set up wtforms class """
    keywords = StringField('query', [
        validators.Length(max=200, message="length"),
        validators.Regexp('^[ a-zA-Z]*$', message="regex")])
    campus = SelectField('Campus', choices=campuschoices,
                         validators=[validators.Required(message="campus")])
    facet = SelectField('Facet', choices=facetchoices,
                        validators=[validators.Required(message="facet")])


@app.route('/')
def index():
    """ show the search form """
    form = SearchForm()
    return render_template("landing.html", displaydata={}, errordata=0,
                           form=form)


@app.route('/submit', methods=['POST'])
def submit():
    """ handle form data and display the results """
    form = SearchForm(request.form)

    handlesession = handlesubmit.managesession(form, campuschoices)
    campus_code = handlesession[0]
    chosencampusname = handlesession[1]
    val = handlesubmit.allvalidate(form, campus_code, chosencampusname)
    if type(val) == list:
        return handlesubmit.makeapicall(campus_code, val[0], form, chosencampusname)
    else:
	return val 

app.secret_key = key

if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
