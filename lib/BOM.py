import csv


class BOM:
	def __init__(self, filename):
		self.filename = filename
		self._header = {}
		self._content = []
		self.__read_csv()

	def __read_csv(self):
		with open(self.filename, 'r') as f:
			bom = csv.reader(f, delimiter=';')

			for row_num, r in enumerate(bom):
				if row_num is 0:
					# parse header
					self._header = r

				else:
					# parse data
					temp = {}
					for col_num, c in enumerate(r):
						temp[self._header[col_num]] = c

					self._content.append(temp)
		f.close()

	def write_csv(self, results):
		with open(self.filename[:-4]+'digikey.csv', 'w') as wf:
			keys = sorted(results[0].keys())
			# swap order of columns for readability
			keys[keys.index('ref')], keys[0] = keys[0], keys[keys.index('ref')]
			keys[keys.index('tol')], keys[keys.index('sku')] = keys[keys.index('sku')], keys[keys.index('tol')]
			writer = csv.DictWriter(wf, keys, lineterminator='\n')

			writer.writeheader()
			for i in range(len(results)):
				# Skip if part not found
				if results[i] is None:
					continue
				# Replace None values with empty cell
				for key in keys:
					if results[i][key] is None:
						results[i][key] = ''
				writer.writerow(results[i])
			wf.close()


	def content(self):
		return self._content
