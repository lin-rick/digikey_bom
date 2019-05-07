import re
import pint
import requests
from bs4 import BeautifulSoup

from lib.digikey.Queries import Queries
from lib.digikey.Types import Comp


class Digikey:
	base_url = "https://www.digikey.ca/products/en/"

	def __init__(self):
		self.queries = Queries()
		self.units = pint.UnitRegistry('lib/digikey/units.txt')

	def get_link(self, digikey_id, tol=None, ref=None):
		url = self.base_url + self.queries.digikey_id + digikey_id
		print('{}: {}'.format(ref, url))

		# Get price and qty
		req = requests.get(url)
		soup = BeautifulSoup(req.text, features="html.parser")
		table = soup.find('table', attrs={'class': "product-dollars"})
		if table is None:
			return {
				'sku': digikey_id,
				'desc': '',
				'price': '',
				'qty': '',
				'url': '',
				'tol': '',
				'ref': ''
			}

		rows = []
		for row in table.find_all("tr")[:]:
			rows.append(row)

		line = str(rows[1]).splitlines()
		price = re.search("[0-9]*\.[0-9]{2}", line[3]).group(0)
		qty = soup.find('span', attrs={'id': 'dkQty'})

		return {
			'sku': digikey_id,
			'desc': '',
			'price': str(price),
			'qty': re.search("[0-9,]{1,10}", str(qty)).group(0),
			'url': self.base_url + self.queries.digikey_id + digikey_id,
			'tol': tol,
			'ref': ref
		}

	def look_for(self, component, value, package, tol=None, ref=None):
		# skip 'do not populate'
		if value is None or 'DNP' in value:
			return

		url = self.generate_query_url(component, value, package, tol)
		print('{}: {}'.format(ref, url))

		req = requests.get(url)
		soup = BeautifulSoup(req.text, features="html.parser")
		table = soup.find(id='lnkPart')

		# part not found
		if table is None:
			print('{}: {} {} {} could not be found'. format(ref, value, package, tol))
			return

		for r in table.find_all('tr'):
			sku = r.find('td', attrs={'class': re.compile('dkpartnumber', re.I)}).text
			desc = r.find('td', attrs={'class': re.compile('description', re.I)}).text
			price = r.find('td', attrs={'class': re.compile('unitprice', re.I)}).text
			qty = r.find('td', attrs={'class': re.compile('qtyavailable', re.I)})
			qty = qty.select_one('span').text.strip()

			return {
				'sku': str(sku).strip(),
				'desc': str(desc).strip(),
				'price': re.search("(?<=\$)[0-9]*\.[0-9]{2}", str(price)).group(0),
				'qty': re.search("[0-9]*[,]?[0-9]*", str(qty)).group(0),
				'url': "https://www.digikey.ca/products/en?keywords=" + str(sku).strip(),
				'tol': tol,
				'ref': ref
			}

	def get_break(self, sku):
		req = requests.get(self.base_url + self.queries.digikey_id + sku)
		soup = BeautifulSoup(req.text, features="html.parser")
		table = soup.find('table', attrs={'class': "product-dollars"})

		if table is None:
			return '', ''

		rows = []
		for row in table.find_all("tr")[:]:
			rows.append(row)

		line = str(rows[2]).splitlines()
		qtybreak = re.search("[0-9]{1,3}", line[1]).group(0)
		pricebreak = re.search("[0-9]*\.[0-9]{2}", line[2]).group(0)

		return qtybreak, pricebreak

	def generate_query_url(self, component, value, package, tol=None):
		url = self.base_url

		# filter component and values
		if component is Comp.resistor:
			url = url + self.queries.resistors_url + self.queries.default_filters
			url = url + self.queries.resistor_value + self.__get_resistance(value)

		elif component is Comp.capacitor_cer:
			url = url + self.queries.capacitors_cer_url + self.queries.default_filters
			url = url + self.queries.capacitor_value + self.__get_capacitance(value)

		elif component is Comp.capacitor_tant:
			url = url + self.queries.capacitors_tant_url + self.queries.default_filters
			url = url + self.queries.capacitor_value + self.__get_capacitance(value)

		elif component is Comp.inductor:
			url = url + self.queries.inductor_url + self.queries.default_filters
			url = url + self.queries.inductor_value + self.__get_inductance(value)

		else:
			raise AttributeError('Component {} not defined'.format(component))

		# filter package
		try:
			url = url + self.__get_package(package)
		except KeyError:
			raise KeyError('{} package size not defined in package_map'.format(package))

		# filter tolerances
		if tol:
			try:
				url = url + self.__get_tolerance(tol)
			except KeyError:
				raise KeyError('{} tolerance not defined in tolerance_map'.format(tol))

		return url

	def __get_resistance(self, value):
		if '{:P}'.format(self.units.ohm) not in value and \
			'{:~}'.format(self.units.ohm) not in value:
			value = self.units.Quantity(value, self.units.ohm)
		return str(value).replace(' ', '')

	def __get_capacitance(self, value):
		if '{:P}'.format(self.units.farad) not in value and \
			'{:~}'.format(self.units.farad) not in value:
			value = self.units.Quantity(value, self.units.farad)
		return str(value).replace(' ', '')

	def __get_inductance(self, value):
		if '{:P}'.format(self.units.henry) not in value and \
			'{:~}'.format(self.units.henry) not in value:
			value = self.units.Quantity(value, self.units.henry)
		return str(value).replace(' ', '')

	def __get_package(self, package):
		return self.queries.package_map[package]

	def __get_tolerance(self, tol):
		return self.queries.tolerance_map[tol]
