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
import logging

import ConfigParser
from SearchModule import *

log = logging.getLogger(__name__)

# Search on Newznab
class ad_NZBclub(SearchModule):
	# Set up class variables
	def __init__(self, configFile=None):
		super(ad_NZBclub, self).__init__()
		# Parse config file		
		self.name = 'NZBClub'
		self.shortName = 'CLB'
		self.queryURL = 'https://www.nzbclub.com/nzbfeed.aspx'
		self.baseURL = 'https://www.nzbclub.com'
		self.active = 1
		self.builtin = 1
		self.login = 0
	# Perform a search using the given query string
	def search(self, queryString, cfg):		
		urlParams = dict(
			q=queryString,
            ig= 1,
            rpp= 200,
            st= 5,
            sp= 1,
            ns= 1
		)
		
		results = SearchResults()
		try:
			http_result = requests.get(url=self.queryURL, params=urlParams, verify=False, timeout=cfg['timeout'])
		except Exception as e:
			log.error('Failed to get response from server: ' + str(e))
			return results
		data = http_result.text
		data = data.replace("<newznab:attr", "<newznab_attr")
		
			
		#~ parse errors
		try:
			tree = ET.fromstring(data.encode('utf-8'))
		except Exception as e:
			log.error('Failed to parse data from server: ' + str(e))
			return results

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
			r.nzbURL = elem_url.attrib['url']
			r.timestamp = int(elem_postdate)
			r.provider = self.name
			r.providerURL = self.baseURL
			
			results.append(r)
		return results		
