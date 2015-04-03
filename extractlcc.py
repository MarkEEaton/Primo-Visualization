import json
import sys
import os

if len(sys.argv) < 2:
	sys.exit('Usage: python extractlcc.py <file>')

if not os.path.exists(sys.argv[1]):
	sys.exit('Error: File %s not found' % sys.argv[1])

fo = open(sys.argv[1], "r")
txt = fo.read();
jsontxt = json.loads(txt)
lcc = (jsontxt['SEGMENTS']['JAGROOT']['RESULT']['FACETLIST']['FACET'][1]['FACET_VALUES'])
print(lcc)

for line in lcc:
	tr = {'@KEY':'name', '@VALUE':'size'}
	newlcc = {tr[k]: v for k, v in line.items()}
	print(newlcc)

with open("tmp2.json", "w") as outfile:
	json.dump(lcc, outfile)
