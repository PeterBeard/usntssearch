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

import time
from operator import itemgetter
from urllib2 import urlparse
from flask import render_template

import SearchModule

def dosearch(strsearch, cfg=None, sortkey='relevance', sortdir='asc', ver_notify=''):
	if cfg == None:
		cfg = {'enabledModules':['nzbX.co','NZB.cc']}
	strsearch = strsearch.strip()
	
	if(len(strsearch)):
		print 'searching'
		results = SearchModule.performSearch(strsearch, cfg)
	else:
		return render_template('main_page.html',vr=ver_notify)
	print 'search complete'
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

