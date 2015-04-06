import json
import sys
import os

changed = []

def extract(jsontxt):
	print "running extract"
	lcc = (jsontxt['SEGMENTS']['JAGROOT']['RESULT']['FACETLIST']['FACET'][1]['FACET_VALUES'])


	def changeKeys(originalJSON):
		for line in originalJSON:
			tr = {'@KEY':'name', '@VALUE':'size'}
			changed.append({tr[k]: v for k, v in line.items()})
			print "running change keys"

	changeKeys(lcc);

	output = {"name": "content", "children": changed}
	print output
	return output
