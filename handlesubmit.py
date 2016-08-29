from flask import (session, render_template, request)
import requests
import json
import extractfromjson


def validateform(form):
    """ validates the form, else returns error codes """
    if form.campus and form.campus.data == "None":
        del form.campus
    if request.method == 'POST' and form.validate():
        return None
    else:
        return form.errors.itervalues().next()


def allvalidate(form, campus_code, chosencampusname):
    """ runs the validation; renders templates if validation fails """
    if validateform(form) is None:
        query = form.keywords.data
        return [query]
    elif "length" in validateform(form):
        return render_template("viz.html", displaydata={},
                               errordata=4, campus=chosencampusname)
    elif "regex" in validateform(form):
        return render_template("viz.html", displaydata={},
                               errordata=2, campus=chosencampusname)
    elif ("facet" or "campus") in validateform(form):
        return render_template("viz.html", displaydata={},
                               errordata=3, campus=chosencampusname)
    else:
        return False


def managesession(form, campuschoices):
    """ handles session data """
    if form.campus.data == "None":
        campus_code = session['campus_code']
        chosencampusname = session['chosencampusname']
        return campus_code, chosencampusname
    else:
        campus_code = form.campus.data
        chosencampusname = dict(campuschoices).get(form.campus.data)
        session['campus_code'] = campus_code
        session['chosencampusname'] = chosencampusname
        return campus_code, chosencampusname


def makeapicall(campus_code, query, form, chosencampusname):
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
