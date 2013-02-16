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
import difflib
import logging
import time

log = logging.getLogger(__name__)

# The set of results returned by a search
class SearchResults(object):
	# Initialize
	def __init__(self):
		self.current = 0
		self.results = []
		pass
	# Make the object iterable
	def __iter__(self):
		return iter(self.results)
	# Add a result (or results) to the set
	def append(self, resultObject):
		if isinstance(resultObject, Result):
			self.results.append(resultObject)
		elif isinstance(resultObject, SearchResults):
			self.results = self.results + resultObject.results
		else:
			raise TypeError('Only Result objects can be appended to a SearchResults object')
	# Sort the results by relevance, i.e. string similarity
	def sortByRelevance(self, queryString=''):
		queryString = queryString.lower()
		dottedQueryString = queryString.replace(' ','.')
		# difflib can be used to calculate the similarities of two strings
		# difflib.SequenceMatcher(isjunk=None, a='', b='', autojunk=True)
		for r in self.results:
			title = r.title.lower()
			try:
				r.score = difflib.SequenceMatcher(None, title, queryString).ratio() + difflib.SequenceMatcher(None, title, dottedQueryString).ratio()
			except Exception as e:
				r.score = 2
				log.error('Error calculating score: ' + str(e))

		# Now, sort the results by score
		self.results.sort(key=lambda x: x.score, reverse=True)
	# Sort the results by age
	# Set direction to 'asc' for ascending or 'desc' for descending
	def sortByAge(self, direction='asc'):
		# Determine sort direction
		if direction.lower() == 'desc':
			reverse = False
		else:
			reverse = True
		# Sort the list
		self.results.sort(key=lambda x: x.timestamp, reverse=reverse)
	# Sort the results by file size
	# Set direction to 'asc' for ascending or 'desc' for descending
	def sortBySize(self, direction='asc'):
		# Determine sort direction
		if direction.lower() == 'desc':
			reverse = True
		else:
			reverse = False
		# Sort the list
		self.results.sort(key=lambda x: x.size, reverse=reverse)
	# Remove duplicate items from the list
	# Doesn't really remove anything, but gives the user a choice of providers where possible
	def removeDuplicates(self):
		pass

# Object to contain data about an NZB search result
class Result(object):
	def __init__(self, title='Not Set', nzbURL='#', nfoURL='#', timestamp=0, age=0, size=0, filesize=0, poster='Not Set', group='Not Set', provider='Not Set', providerURL='#'):
		self.title = title
		self.nzbURL = nzbURL
		self.nfoURL = nfoURL
		self.timestamp = timestamp
		self.age = age
		self.size = size
		self.filesize = filesize
		
		self.poster = poster
		self.group = group
		
		self.provider = provider
		self.providerURL = providerURL
	# Calculate the age of the post in days
	def calculateAge(self):
		if self.age == 0:
			# Calculate age in seconds
			currentTime = time.time()
			age = currentTime - self.timestamp
			# Hours
			age = age/3600
			if age < 24:
				self.age = str(int(round(age))) + ' h'
			else:
				self.age = str(int(round(age/24))) + ' d'
		return self.age
	# Calculate the nearest SI unit to use for the size
	def siSize(self):
		if self.filesize == 0:
			# Keep dividing the size until it's less than 1000
			reducedSize = self.size
			units = ['','k','M','G','T']
			unitIndex = 0
			while reducedSize >= 1000.0:
				unitIndex = unitIndex + 1
				reducedSize = reducedSize / 1000
			self.filesize = str(int(reducedSize*10)/10) + ' ' + units[unitIndex] + 'B'
		return self.filesize
