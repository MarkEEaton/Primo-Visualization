def extract(jsontxt, radiochoice):

    # set default values of variables
    changed = []
    errorcheck = False

    # parse data based on radio button selected. Returns error if it fails.
    try:
        fulldata = (jsontxt['SEGMENTS']['JAGROOT']['RESULT']['FACETLIST']
                    ['FACET'])
        for facet in fulldata:
            if facet['@NAME'] == radiochoice:
                choicedata = facet['FACET_VALUES']
                errorcheck = True
    except:
        errorcheck = False

    # change the keys in the json to what is needed by the d3 script
    def changeKeys(originalJSON):
        for line in originalJSON:
            tr = {'@KEY': 'name', '@VALUE': 'size'}
            changed.append({tr[k]: v for k, v in line.items()})
        return

    # make choicedata a list if it is not a list
    def makelist(originaldata):
        if type(originaldata) is list:
            return originaldata
        elif type(originaldata) is dict:
            changeddata = [originaldata]
            return changeddata
        else:
            print "is not a dict or a list."

    # if error free, return use-ready json, else return False
    if errorcheck is True:
        changeKeys(makelist(choicedata))
        output = {"name": "content", "children": changed}
        return output
    else:
        return False
