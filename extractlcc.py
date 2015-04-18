import json
import sys
import os
import pdb

def extract(jsontxt, radiochoice):
	changed = []
	errorcheck = False
	print "running extract"
	try:
		if radiochoice == "lcc":
			choicedata = (jsontxt['SEGMENTS']['JAGROOT']['RESULT']['FACETLIST']['FACET'][1]['FACET_VALUES'])
			errorcheck = True
		elif radiochoice == "date":
			choicedata = (jsontxt['SEGMENTS']['JAGROOT']['RESULT']['FACETLIST']['FACET'][8]['FACET_VALUES'])
			errorcheck = True
		else:
			print 'No choice selected'
			choicedata = {}
			errorcheck = False 
	except:
		print('Term not found')
		errorcheck = False

	def changeKeys(originalJSON):
		for line in originalJSON:
			tr = {'@KEY':'name', '@VALUE':'size'}
			changed.append({tr[k]: v for k, v in line.items()})
			print "running change keys"

	if errorcheck == True:
		changeKeys(choicedata);
		output = {"name": "content", "children": changed}
		return output
	else:
		print('returning false')
		return False
