import json
import sys
import os

def extract(jsontxt, radiochoice):
	
    # set default values of variables
    changed = []
    errorcheck = False

    # parse data based on radio button selected. Returns error if it fails.
    try:
        if radiochoice == "lcc":
            choicedata = (jsontxt['SEGMENTS']['JAGROOT']['RESULT']['FACETLIST']['FACET'][1]['FACET_VALUES'])
            errorcheck = True
        elif radiochoice == "date":
            choicedata = (jsontxt['SEGMENTS']['JAGROOT']['RESULT']['FACETLIST']['FACET'][8]['FACET_VALUES'])
            errorcheck = True
        elif radiochoice == "genre":
            choicedata = (jsontxt['SEGMENTS']['JAGROOT']['RESULT']['FACETLIST']['FACET'][9]['FACET_VALUES'])
            errorcheck = True
        else:
            print 'No choice selected'
            choicedata = {}
            errorcheck = False 
    except:
        print('Term not found')
        errorcheck = False

    # change the keys in the json to what is needed by the d3 script
    def changeKeys(originalJSON):
        for line in originalJSON:
            tr = {'@KEY':'name', '@VALUE':'size'}
            changed.append({tr[k]: v for k, v in line.items()})

    # if error free, return use-ready json, else return False
    if errorcheck == True:
        changeKeys(choicedata);
        output = {"name": "content", "children": changed}
        return output
    else:
        return False
