# # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## #    
#~ This file is part of NZBmegasearch by 0byte.
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
from urllib2 import urlparse


# Search on Newznab
class Newznab(SearchModule):
					
	# Set up class variables
	def __init__(self, configFile=None):
		super(Newznab, self).__init__()
		# Parse config file		
		self.name = 'Newznab'
		self.typesrch = 'NAB'
		self.queryURL = 'xxxx'
		self.baseURL = 'xxxx'
		self.nzbDownloadBaseURL = 'NA'
		self.builtin = 0
		self.inapi = 1
		self.api_catsearch = 1
		self.agent_headers = {	'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' }	
		
		self.categories = {'Console': {'code':[1000,1010,1020,1030,1040,1050,1060,1070,1080], 'pretty': 'Console'},
							'Movie' : {'code': [2000, 2010, 2020], 'pretty': 'Movie'},
 							'Movie_HD' : {'code': [2040, 2050, 2060], 'pretty': 'HD'},
							'Movie_SD' : {'code': [2030], 'pretty': 'SD'},
							'Audio' : {'code': [3000, 3010, 3020, 3030, 3040], 'pretty': 'Audio'},
							'PC' : {'code': [4000, 4010, 4020, 4030, 4040, 4050, 4060, 4070], 'pretty': 'PC'},
							'TV' : {'code': [5000,  5020], 'pretty': 'TV'},
							'TV_SD' : {'code': [5030], 'pretty': 'SD'},
							'TV_HD' : {'code': [5040], 'pretty': 'HD'},
							'XXX' : {'code': [6000, 6010, 6020, 6030, 6040], 'pretty': 'XXX'},
							'Other' : {'code': [7000, 7010], 'pretty': 'Other'},
							'Ebook' : {'code': [7020], 'pretty': 'Ebook'},
							'Comics' : {'code': [7030], 'pretty': 'Comics'},
							} 
		self.category_inv= {}
		for key in self.categories.keys():
			prettyval = self.categories[key]['pretty']
			for i in xrange(len(self.categories[key]['code'])):
				val = self.categories[key]['code'][i]
				self.category_inv[str(val)] = prettyval
		#~ print self.category_inv
	
	#~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
	def search_raw(self, queryopt, cfg):
		urlParams = dict(
			queryopt,
			o='xml',
			apikey=cfg['api']
		)
		self.queryURL = cfg['url'] + '/api'
		self.baseURL = cfg['url']
		
		parsed_data = self.parse_xmlsearch(urlParams, cfg['timeout'])		
		return parsed_data		
	
	#~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

	def search(self, queryString, cfg):
		# Get text
		urlParams = dict(
			t='search',
			q=queryString,
			o='xml',
			apikey=cfg['api']
		)
		self.queryURL = cfg['url'] + '/api'
		self.baseURL = cfg['url']
		
		'''
		try:
			http_result = requests.get(url=baseURL, params=urlParams, verify=False, timeout=cfg['timeout'])
		except Exception as e:
			print e
			return []
		data = http_result.text

		# Try to parse the data
		results = SearchResults()

		data = data.replace("<newznab:attr", "<newznab_attr")

		#~ parse errors
		try:
			tree = ET.fromstring(data.encode('utf-8'))
		except BaseException:
			print "ERROR: Wrong API?"
			return results
		except Exception as e:
			print e
			return results

		#~ homemade lazy stuff
		humanprovider = urlparse.urlparse(cfg['url']).hostname			
		humanprovider = humanprovider.replace("www.", "")


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
			r = Result()
			r.title = elem_title.text
			r.poster = elem_poster
			r.size = int(elem_url.attrib['length'])
			r.timestamp = float(elem_postdate)
			r.nzbURL = elem_url.attrib['url']
			r.provider = self.name
			r.providerURL = self.baseURL

			results.append(r)
		return results
	# Show config options
	def configurationHTML(self):
		htmlBuffer = '-- Newznab Options --'
		return htmlBuffer
	'''
		#~ homemade lazy stuff
		humanprovider = urlparse.urlparse(cfg['url']).hostname			
		self.name = humanprovider.replace("www.", "")
		parsed_data = self.parse_xmlsearch(urlParams, cfg['timeout'])			
		return parsed_data

