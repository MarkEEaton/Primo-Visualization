from flask import (Flask, render_template, request, session)
from wtforms import *
import requests
import extractfromjson
import json
import re
import ast

app = Flask(__name__)

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

class SearchForm(Form):
    keywords = StringField('query', [
               validators.Length(max=200, message="length"), 
               validators.Regexp('^[ a-zA-Z]*$', message="regex")])
    campus = SelectField('Campus', choices=campuschoices,
               validators=[validators.Required(message="campus")])

@app.route('/')
def index():
    form = SearchForm()
    return render_template("landing.html", displaydata={}, errordata=0, form=form)


@app.route('/submit', methods=['POST'])
def submit():
    form = SearchForm(request.form)

    def validateform(form):
        if request.method == 'POST' and form.validate():
            global query
            query = form.keywords.data 
            return True
        else:
            print "returning false" 
            return form.errors['keywords'][0]

    # extract campus info from the form, otherwise extract from the session
 
    try:
        chosencampus = form.campus
        print "loaded campus from form"
    except:
        chosencampus = session['campus']
        print "loaded campus from sesssion"
        pass
    else:
        print "else firing"
        print validateform(form)
        if validateform(form) == "campus":
            print "failed validation"
            return render_template("viz.html", displaydata={},
                                   errordata=3, campus=chosencampus)
        else:
            print "loaded campus into session"
            session['campus'] = form.campus
            pass


    # validate length and characters in query
    if validateform(form) == "length":
        return render_template("viz.html", displaydata={},
                               errordata=4, campus=chosencampus)
    elif validateform(form) == "regex":
        return render_template("viz.html", displaydata={},
                               errordata=2, campus=chosencampus)
    else:
        pass

    # validaVte dropdown menu
    choice = request.form['type']
    correct_choices = set(['lcc', 'creationdate', 'topic'])
    if choice not in correct_choices:
        return render_template("viz.html", displaydata={},
                               errordata=3, campus=chosencampus)

    # make an api request using the inserting the query variable in the url
    campus_code = form.campus.data
    print campus_code
    print query
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
                               campus=chosencampus)
    else:
        return render_template("viz.html", displaydata=readydata,
                               errordata=0, val=query, campus=chosencampus)

app.secret_key = 'key goes here'

if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1', debug=True)
