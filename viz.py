from flask import (Flask, render_template, request)
from wtforms import *
import handlesubmit
from key import appkey

app = Flask(__name__)


facet_choices = [('lcc', 'Library of Congress Classification'),
                 ('creationdate', 'Creation Date'),
                 ('topic', 'Topic')]
campus_choices = [('BB', 'Baruch'),
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
    campus = SelectField('Campus', choices=campus_choices,
                         validators=[validators.Required(message="campus")])
    facet = SelectField('Facet', choices=facet_choices,
                        validators=[validators.Required(message="facet")])


@app.route('/')
def index():
    """ show the search form """
    form = SearchForm()
    return render_template("landing.html", display_data={}, errordata=0,
                           form=form)


@app.route('/submit', methods=['POST'])
def submit():
    """ handle form data and display the results """
    form = SearchForm(request.form)

    campus_code = handlesubmit.manage_session(form, campus_choices)[0]
    chosen_campus_name = handlesubmit.manage_session(form, campus_choices)[1]
    val = handlesubmit.all_validate(form, campus_code, chosen_campus_name)
    if type(val) == list:
        return handlesubmit.make_api_call(campus_code, val[0],
                                          form, chosen_campus_name)
    else:
        return val

app.secret_key = appkey

if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1', debug=True)
