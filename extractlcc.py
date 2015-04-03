import json
import sys
import os

changed = []

if len(sys.argv) < 2:
	sys.exit('Usage: python extractlcc.py <file>')

if not os.path.exists(sys.argv[1]):
	sys.exit('Error: File %s not found' % sys.argv[1])

fo = open(sys.argv[1], "r")
jsontxt = json.loads(fo.read())
lcc = (jsontxt['SEGMENTS']['JAGROOT']['RESULT']['FACETLIST']['FACET'][1]['FACET_VALUES'])

def changeKeys(originalJSON):
	for line in originalJSON:
		tr = {'@KEY':'name', '@VALUE':'size'}
		changed.append({tr[k]: v for k, v in line.items()})

changeKeys(lcc);

output = {"name": "content", "children": changed}
print(output)

with open("tmp2.json", "w") as outfile:
	json.dump(output, outfile)
