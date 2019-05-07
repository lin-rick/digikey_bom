import re
from lib.digikey.Digikey import Digikey
from lib.digikey.Types import Comp
from lib.BOM import BOM
import os

results = []
HW_VERSION = input("Please enter the HW Version Number: (ie. 8.0)\n")
EAGLE_DIR = input("Please enter the full path to the Eagle directory: (ie. C:\\Eagle 9.2.0)\n")
PYTHON_DIR = os.getcwd()
SCH_DIR = PYTHON_DIR + "\\..\\..\\hardware\\v{}\\{}.sch".format(HW_VERSION[0], HW_VERSION)

if __name__ == "__main__":

	# Run Eagle ULP to generate component list
	os.chdir(EAGLE_DIR)
	t = os.system('eaglecon.exe \"{}\" -C \" RUN {} {}; quit;\"'
					.format(SCH_DIR, PYTHON_DIR+'\\movitbom.ulp', PYTHON_DIR+'\\'+HW_VERSION+'.csv'))

	os.chdir(PYTHON_DIR)
	bm = BOM(HW_VERSION + '.csv')
	dk = Digikey()

	for c in bm.content():
		# check for digikey product id
		if 'DIGIKEY' in c.keys() and len(c['DIGIKEY']) > 0:
			result = dk.get_link(c['DIGIKEY'], ref=c['Parts'])
			qtybreak, pricebreak = dk.get_break(result['sku'])
			result['qtybreak'], result['pricebreak'] = qtybreak, pricebreak
			results.append(result)
			continue

		# get component
		comp = None
		if re.search('^R[0-9]{4}', c['Device']):
			comp = Comp.resistor

		elif re.search('^C[0-9]{4}_TANT', c['Device']):
			comp = Comp.capacitor_tant

		elif re.search('^C[0-9]{4}', c['Device']):
			comp = Comp.capacitor_cer

		elif re.search('^L[0-9]{4}', c['Device']):
			comp = Comp.inductor

		else:
			print('{} PART NOT FOUND'.format(c['Parts']))

		# get component value
		val = c['Value'] if 'Value' in c.keys() else None

		# get component package size
		pack = c['Package'] if 'Package' in c.keys() else None

		# get component tolerance
		tol = c['TOL'] if 'TOL' in c.keys() and len(c['TOL']) > 0 else None

		# get part reference
		ref = c['Parts'] if 'Parts' in c.keys() else None

		if comp is not None:
			result = dk.look_for(comp, val, pack, tol, ref)
			if result is not None:
				qtybreak, pricebreak = dk.get_break(result['sku'])
				result['qtybreak'], result['pricebreak'] = qtybreak, pricebreak
			results.append(result)

	bm.write_csv(results)
