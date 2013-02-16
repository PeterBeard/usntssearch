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
import cPickle as pickle
import hashlib
import logging
import os
import time

from flask import render_template
from operator import itemgetter
from urllib2 import urlparse

import SearchModule

log = logging.getLogger(__name__)

def dosearch(strsearch, cfg=None, sortkey='relevance', sortdir='asc', ver_notify='', max_cache_age=0):
	if cfg == None:
		cfg = {'enabledModules':['nzbX.co','NZB.cc'],'max_cache_age':'0'}
	strsearch = strsearch.strip()
	
	if(len(strsearch)):
		cachename = hashlib.md5(strsearch).hexdigest()
		cachepath = 'cache/' + cachename + '.p'
		# See if a cached version of the results is available
		try:
			# See how old the file is
			age = (time.time() - os.stat(cachepath).st_mtime)/3600
			if age > max_cache_age:
				raise IOError('Cache too old; maximum age is ' + str(max_cache_age) + ' hours.')
			else:
				results = pickle.load(open(cachepath,'rb'))
		except IOError as e:
			log.warning('Failed to use cached search result: ' + str(e))
			results = SearchModule.performSearch(strsearch, cfg)
			pickle.dump(results, open(cachepath,'wb'))
		except Exception as e:
			log.warning('Exception while accessing cached file: ' + str(e))
			results = SearchModule.performSearch(strsearch, cfg)
			pickle.dump(results, open(cachepath,'wb'))
	else:
		return render_template('main_page.html',vr=ver_notify)
	# Sort the results
	if sortkey == 'age': # By age
		results.sortByAge(sortdir)
	elif sortkey == 'size': # By size
		results.sortBySize(sortdir)
	else:
		results.sortByRelevance(strsearch)
	# Render the page
	return render_template('main_page.html',results=results,sortkey=sortkey,sortdir=sortdir,queryString=strsearch,vr=ver_notify)

def sanitize_html(value):
	if(len(value)):
		value = value.replace("<\/b>", "")
		value = value.replace("<b>", "")
		value = value.replace("&quot;", "")	
	return value

#~ debug
if __name__ == "__main__":
	print 'Save to file'
	webbuf_ret = dosearch('Hotel.Impossible.S01E01')
	myFile = open('results.html', 'w')
	myFile.write(webbuf_ret)
	myFile.close()

