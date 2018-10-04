""" SeeCollections """
import json
from flask import Flask, render_template, request
from wtforms import Form, SelectField, StringField, validators
import requests
from key import apikey

app = Flask(__name__)


class SearchForm(Form):
    """ set up wtforms class """
    facet_choices = [('lcc', 'Library of Congress Classification'),
                     ('creationdate', 'Creation Date'),
                     ('topic', 'Topic')]

    college_choices = [('BB', 'Baruch'),
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
                       ('YC', 'York')]

    college = SelectField('college',
                          choices=college_choices,
                          validators=[validators.DataRequired(message='You must select a campus.')])
    facet = SelectField('facet',
                        choices=facet_choices,
                        validators=[validators.DataRequired(message='You must select a facet.')])
    keyword = StringField('keyword', [
        validators.Length(max=200, message='You cannot enter more than 200 characters.'),
        validators.Regexp(r'^[\-a-zA-Z ]*$',
                          message='Invalid characters in your search string. \
                                   Use only A-Z, -, and space.'),
        validators.DataRequired(message='You must type in something.')])

@app.route('/', methods=['GET', 'POST'])
def index():
    """ display the index page """
    form = SearchForm(request.form)
    faux_data = {"name": "content", "children": None}

    if request.method == 'GET':
        return render_template('index.html', error_message='', final_data=faux_data, form=form)

    else:
        if form.validate():
            get_facet = request.form['facet']
            get_college = request.form['college']
            get_keyword = request.form['keyword']
            resp = requests.get('https://api-na.hosted.exlibrisgroup.com/primo/v1/'
                                'search?vid=CUNY&scope=everything'
                                '&q=any,contains,{}&qInclude=facet_local3,exact,{}'
                                '&qInclude=facet_rtype,exact,books'
                                '&apikey={}'.format(get_keyword, get_college, apikey))


            api_call = json.loads(resp.text)

            # what if there are no results?
            if api_call['facets'] == []:
                error_message = "<div class='alert alert-danger' role='alert'>No results found!</div>"
                return render_template('index.html', error_message=error_message,
                                   final_data=faux_data, form=form)

            # parse the api data 
            facet_data = api_call['facets']
            for facet in facet_data:
                if facet['name'] == get_facet:
                    chosen_facet = facet['values']

            # make chosen_facet a list if it is not a list
            # this will happen if there is only one result
            if isinstance(chosen_facet, dict):
                chosen_facet = [chosen_facet]

            # transform the data into a format d3 will like
            transformed_facet = []
            for line in chosen_facet:
                temp = {'value': 'name', 'count': 'size'}
                transformed_facet.append({temp[k]: v for k, v in line.items()})

            final_data = {"name": "content", "children": transformed_facet}

            return render_template("index.html", error_message='',
                                   final_data=final_data, form=form)
        else:
            error_message = "<div class='alert alert-danger' role='alert'>" + form.errors['keyword'][0] + "</div>"
            return render_template('index.html', error_message=error_message,
                                   final_data=faux_data, form=form)


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1', debug=True)
