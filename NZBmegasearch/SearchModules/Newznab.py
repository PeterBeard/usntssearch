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
	 
	# Perform a search using the given query string
	def search(self, queryString, cfg):
		# Get text
		urlParams = dict(
			t='search',
			q=queryString,
			o='xml',
			apikey=cfg['api']
		)
		baseURL = cfg['url'] + '/api'
		
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
