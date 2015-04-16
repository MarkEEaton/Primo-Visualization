import json
import sys
import os
import pdb

def extract(jsontxt):
	changed = []
	errorcheck = False
	print "running extract"
	try:
		lcc = (jsontxt['SEGMENTS']['JAGROOT']['RESULT']['FACETLIST']['FACET'][1]['FACET_VALUES'])
		errorcheck = True
	except:
		print('Term not found')
		errorcheck = False

	def changeKeys(originalJSON):
		for line in originalJSON:
			tr = {'@KEY':'name', '@VALUE':'size'}
			changed.append({tr[k]: v for k, v in line.items()})
			print "running change keys"

	if errorcheck == True:
		changeKeys(lcc);
		output = {"name": "content", "children": changed}
		return output
	else:
		print('returning false')
		return False
