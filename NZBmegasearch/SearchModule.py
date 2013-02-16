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
import config_settings
import logging
import os
import requests
import threading
import time

from SearchResults import *

log = logging.getLogger(__name__)

def loadSearchModules(moduleDir = None):
	global loadedModules
	# Find search modules
	loadedModules = [];
	searchModuleNames = [];
	if moduleDir == None:
		moduleDir = os.path.join(os.path.dirname(__file__),'SearchModules');
	log.info('Loading modules from: ' + moduleDir)

	for file in os.listdir(moduleDir):
		if file.endswith('.py') and file != '__init__.py':
			searchModuleNames.append(file[0:-3])
	if len(searchModuleNames) == 0:
		log.warning('No search modules found.')
		return
	else:
		log.info('Found ' + str(len(searchModuleNames)) + ' modules')
		
	searchModuleNames = sorted(searchModuleNames)
	# Import the modules that the user has enabled
	log.info('Importing: ' + ', '.join(searchModuleNames))
	
	for module in searchModuleNames:
		try:
			importedModules = __import__('SearchModules.' + module)
		except Exception as e:
			searchModuleNames.remove(module)
			log.error('Failed to import search module "' + module + '": ' + str(e))
	
	log.info('Instantiating module classes')
	# Instantiate the modules
	for module in searchModuleNames:
		try:
			targetClass = getattr(importedModules, module)
			targetClass = getattr(targetClass, module)
		except Exception as e:
			print 'Unable to load search module ' + module + ': ' + str(e)
		
		try:
			loadedModules.append(targetClass())
		except Exception as e:
			log.error('Failed to instantiate search module ' + module + ': ' + str(e))
	log.info('Module loading complete.')

# Perform a search using all available modules
def performSearch(queryString,  cfg):
	queryString = queryString.strip()
	# Perform the search using every module
	global globalResults
	# Load the modules if it hasn't already been done
	if 'loadedModules' not in globals():
		loadSearchModules()
	# Iterate over all of the modules and start a thread for each one to perform its search
	print 'Trying to start ' + str(len(cfg)) + ' search threads.'
	globalResults = SearchResults()
	threadHandles = []
	lock = threading.Lock()
	
	for index in xrange(len(cfg)):
		if(cfg[index]['valid']== '1'):
			try:
				t = threading.Thread(target=performSearchThread, name=cfg[index]['shortName'], args=(queryString,loadedModules,lock,cfg[index]))
				t.start()
				threadHandles.append(t)

			except Exception as e:
				log.error('Error starting thread for search module ' + module + ': ' + str(e))
	# Wait for all the threads to finish
	for t in threadHandles:
		t.join()
	print '=== All Search Threads Finished ==='

	return globalResults

# The thread that performs searches and integrates the results from the various modules
def performSearchThread(queryString, loadedModules, lock, cfg):
	localResults = SearchResults()
	log.info("Searching on " + cfg['shortName'] + " [T" + str(threading.current_thread().ident) + "]")
	for module in loadedModules:
		if module.shortName == cfg['shortName']:
			try:
				localResults = module.search(queryString, cfg)
			except Exception as e:
				log.error('Module ' + module.name + ' failed to perform search: ' + str(e))
	lock.acquire()
	globalResults.append(localResults)
	try:
		lock.release()
	except Exception as e:
		log.error('Could not release search result lock: ' + str(e))

# Exception to be raised when a search function is not implemented
class NotImplementedException(Exception):
	def __init__(self, value):
		self.value = value
	
	def __str__(self):
		return repr(self.value)

# All search modules inherit from this class
class SearchModule(object):
	# Set up class variables
	def __init__(self):
		self.name = 'Unnamed'
		self.shortName = 'UNA'
		self.queryURL = ''
		self.baseURL = ''
		self.nzbDownloadBaseURL = ''
		self.apiKey = ''
		self.userAgent = ''
		self.builtin = 0
		self.login = 0
		self.active = 0
	# Show the configuration options for this module
	def configurationHTML(self):
		return ''
	# Perform a search using the given query string
	def search(self, queryString, cfg):
		raise NotImplementedException('This scraper does not have a search function.')
