# # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## #    
#~ This file is part of NZBmegasearch by pillone.
#~ 
#~ NZBmegasearch is free software: you can redistribute it and/or modify
#~ it under the terms of the GNU General Public License as published by
#~ the Free Software Foundation, either version 3 of the License, or
#~ (at your option) any later version.
#~ 
#~ NZBmegasearch is distributed in the hope that it will be useful,
#~ but WITHOUT ANY WARRANTY; without even the implied warranty of
#~ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#~ GNU General Public License for more details.
#~ 
#~ You should have received a copy of the GNU General Public License
#~ along with NZBmegasearch.  If not, see <http://www.gnu.org/licenses/>.
# # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## #
import ConfigParser
import json
import xml.etree.cElementTree as ET
from SearchModule import *

# Search on Newznab
class Newznab(SearchModule):
	# Set up class variables
	def __init__(self, configFile=None):
		super(Newznab, self).__init__()
		if configFile == None:
			configFile = os.path.join(os.path.dirname(__file__),'Newznab.ini')
		# Parse config file
		parser = ConfigParser.SafeConfigParser()
		parser.read(configFile)
		
		self.name = 'Newznab'
		self.baseURL = parser.get('NewznabConfig','baseURL')
		self.queryURL = self.baseURL + '/api'
		self.apiKey = parser.get('NewznabConfig','apiKey')
	# Perform a search using the given query string
	def search(self, queryString):
		# Get text
		urlParams = dict(
			t='search',
			q=queryString,
			o='xml',
			apikey=self.apiKey
		)
		
		try:
			http_result = requests.get(url=self.queryURL, params=urlParams, verify=False)
		except Exception as e:
			print e
			return []
		data = http_result.text

		# Try to parse the data
		parsed_data = []
		#~ parse errors
		try:
			tree = ET.fromstring(data)
		except BaseException:
			print "ERROR: Wrong API?"
			return parsed_data
		except Exception as e:
			print e
			return parsed_data

		#~ successful parsing
		for elem in tree.iter('item'):
			elem_title = elem.find("title")
			elem_url = elem.find("enclosure")
			elem_pubdate = elem.find("pubDate")
			len_elem_pubdate = len(elem_pubdate.text)
			#~ Tue, 22 Jan 2013 17:36:23 +0000
			#~ removes gmt shift
			elem_postdate =  time.mktime(datetime.datetime.strptime(elem_pubdate.text[0:len_elem_pubdate-6], "%a, %d %b %Y %H:%M:%S").timetuple())
			elem_poster = ''
			
			for attr in elem.iter('newznab_attr'):
				if('name' in attr.attrib):
					if (attr.attrib['name'] == 'poster'): 
						elem_poster = attr.attrib['value']

			d1 = { 
				'title': elem_title.text,
				'poster': elem_poster,
				'size': int(elem_url.attrib['length']),
				'url': elem_url.attrib['url'],
				'filelist_preview': '',
				'group': '',
				'posting_date_timestamp': float(elem_postdate),
				'release_comments': '',
				'ignore':0,
				'provider':self.baseURL
			}
			parsed_data.append(d1)
		return parsed_data
	# Show config options
	def configurationHTML(self):
		htmlBuffer = '-- Newznab Options --'
		return htmlBuffer