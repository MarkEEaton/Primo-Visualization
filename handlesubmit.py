from flask import (session, render_template, request)
import requests
import json
import extractfromjson


def validate_form(form):
    """ validates the form, else returns error codes """
    if form.campus and form.campus.data == "None":
        del form.campus
    if request.method == 'POST' and form.validate():
        return None
    else:
        return form.errors.itervalues().next()


def all_validate(form, campus_code, chosen_campus_name):
    """ runs the validation; renders templates if validation fails """
    if validate_form(form) is None:
        query = form.keywords.data
        return [query]
    elif "length" in validate_form(form):
        return render_template("viz.html", display_data={},
                               error_data=4, campus=chosen_campus_name)
    elif "regex" in validate_form(form):
        return render_template("viz.html", display_data={},
                               error_data=2, campus=chosen_campus_name)
    elif ("facet" or "campus") in validate_form(form):
        return render_template("viz.html", display_data={},
                               error_data=3, campus=chosen_campus_name)
    else:
        return False


def manage_session(form, campus_choices):
    """ handles session data """
    if form.campus.data == "None":
        campus_code = session['campus_code']
        chosen_campus_name = session['chosen_campus_name']
        return campus_code, chosen_campus_name
    else:
        campus_code = form.campus.data
        chosen_campus_name = dict(campus_choices).get(form.campus.data)
        session['campus_code'] = campus_code
        session['chosen_campus_name'] = chosen_campus_name
        return campus_code, chosen_campus_name


def make_api_call(campus_code, query, form, chosen_campus_name):
    """ make the api call and pass the data to extract() """

    # make an api request using the inserting the query variable in the url
    resp = requests.get('http://onesearch.cuny.edu/PrimoWebServices'
                        '/xservice/search/brief?&institution={}&'
                        'query=any,contains,{}&query=facet_rtype,exact,'
                        'books&indx=1&loc=local,scope:'
                        '(KB,AL,CUNY_BEPRESS)&'
                        'loc=adaptor,primo_central_multiple_fe'
                        '&json=true'.format(campus_code, query))

    # assign the api data to a variable, pass it to the parsing function
    api_call = json.loads(resp.text)
    ready_data = extractfromjson.extract(api_call, form.facet.data)

    # if the parsing function fails, dispaly an error, else display
    # viz.html with data
    if ready_data is False:
        return render_template("viz.html", display_data={}, error_data=1,
                               campus=chosen_campus_name)
    else:
        return render_template("viz.html", display_data=ready_data,
                               error_data=0, val=query,
                               campus=chosen_campus_name)
