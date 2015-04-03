import json
import sys
import os

if len(sys.argv) < 2:
	sys.exit('Usage: python extract.py <file>')

if not os.path.exists(sys.argv[1]):
	sys.exit('Error: File %s not found' % sys.argv[1])

fo = open(sys.argv[1], "r")
txt = fo.read();
jsontxt = json.loads(txt)
rtype = (jsontxt['SEGMENTS']['JAGROOT']['RESULT']['FACETLIST']['FACET'][1]['FACET_VALUES'])
print(rtype)

with open("tmp2.json", "w") as outfile:
	json.dump(rtype, outfile)
