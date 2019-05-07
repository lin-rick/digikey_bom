class Queries:
	# urls
	resistors_url = 'resistors/chip-resistor-surface-mount/52?FV='
	capacitors_cer_url = 'capacitors/ceramic-capacitors/60?FV='
	capacitors_tant_url = 'capacitors/tantalum-capacitors/59?FV='
	inductor_url = 'inductors-coils-chokes/fixed-inductors/71?FV='

	# default filters
	cut_tape = "&pv7=2"
	in_stock = "&stock=1"
	min_qty = "&quantity=1"
	sort_price = "&ColumnSort=1000011"

	# keyword search
	digikey_id = '?keywords='

	# value
	resistor_value = '&pv2085=u'
	capacitor_value = '&pv2049=u'
	inductor_value = '&pv2087=u'

	# packages
	package_map = {
		'0402': '&pv16=4',
		'0603': '&pv16=5',
		'0805': '&pv16=6',
		'1206': '&pv16=7'
	}

	# tolerances
	tolerance_map = {
		'0.01%': '&pv3=431',
		'0.02%': '&pv3=357',
		'0.05%': '&pv3=380',
		'0.1%': '&pv3=370',
		'0.25%': '&pv3=377',
		'0.5%': '&pv3=355',
		'1%': '&pv3=1',
		'2%': '&pv3=4',
		'3%': '&pv3=105',
		'5%': '&pv3=2',
		'10%': '&pv3=3',
		'20%': '&pv3=5',

		'0.05pF': '&pv3=75',
		'0.075pF': '&pv3=76',
		'0.25pF': '&pv3=10',
		'0.1pF': '&pv3=77',
		'0.5pF': '&pv3=9',

		'0.05nH': '&pv3=24',
		'0.1nH': '&pv3=127',
		'0.2nH': '&pv3=35',
		'0.3nH': '&pv3=34',
		'0.5nH': '&pv3=74',
	}

	@property
	def default_filters(self):
		return self.cut_tape + self.in_stock + self.min_qty + self.sort_price
