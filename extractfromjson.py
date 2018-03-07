def extract(jsontxt, radiochoice):

    # set default values of variables
    changed = []
    errorcheck = False

    # parse data based on radio button selected. Returns error if it fails.
    try:
        fulldata = (jsontxt['facets'])
        for facet in fulldata:
            if facet['name'] == radiochoice:
                choicedata = facet['values']
                errorcheck = True
    except:
        errorcheck = False

    # change the keys in the json to what is needed by the d3 script
    def changeKeys(original_json):
        pprint(original_json)
        for line in original_json:
            tr = {'value': 'name', 'count': 'size'}
            changed.append({tr[k]: v for k, v in line.items()})
        return

    # make choicedata a list if it is not a list
    def makelist(originaldata):
        if type(originaldata) is list:
            return originaldata
        elif type(originaldata) is dict:
            return [originaldata]
        else:
            print("is not a dict or a list.")

    # if error free, return use-ready json, else return False
    if errorcheck is True:
        changeKeys(makelist(choicedata))
        return {"name": "content", "children": changed}
    else:
        return False
