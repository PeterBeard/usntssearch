# # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## #    
#~ This file is part of NZBmegasearch by pillone.
#~ 
#~ NZBmegasearch is free software: you can redistribute it and/or modify
#~ it under the terms of the GNU General Public License as published by
#~ the Free Software Foundation, either version 3 of the License, or
#~ (at your option) any later version.
#~ 
#~ Foobar is distributed in the hope that it will be useful,
#~ but WITHOUT ANY WARRANTY; without even the implied warranty of
#~ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#~ GNU General Public License for more details.
#~ 
#~ You should have received a copy of the GNU General Public License
#~ along with NZBmegasearch.  If not, see <http://www.gnu.org/licenses/>.
# # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## #    

from flask import render_template
from ConfigParser import SafeConfigParser
import sys
import os
import SearchModule
MAX_PROVIDER_NUMBER = 10

# Write to the configuration file
def	write_conf(requestForm):
	parser = SafeConfigParser()
	parser.read('settings.ini')
	
	# Search modules
	postedEnabledModules = requestForm.getlist('modules')
	parser.set('searchModules','enabledModules',','.join(postedEnabledModules))
	
	# General Settings
	parser.set('general','host',requestForm['host'])
	parser.set('general','port',requestForm['port'])
	parser.set('general','firstRun','0')

	with open('settings.ini', 'wt') as configfile:
		parser.write(configfile)
   
# Read from the configuration file
def read_conf(): 
	cfg_struct = {}
	parser = SafeConfigParser()		
	parser.read('settings.ini')
	# General settings
	cfg_struct['host'] = parser.get('general','host')
	cfg_struct['port'] = parser.get('general','port')
	cfg_struct['firstRun'] = parser.get('general','firstRun')
	# Enabled search modules
	cfg_struct['enabledModules'] = parser.get('searchModules','enabledModules').split(',')

	return cfg_struct

# Build HTML for the configuration page
def html_output(configOptions, optionNames=None):
	if optionNames == None:
		optionNames = {'host':'Host','port':'Port (1024-65535)'}

	modulesHTML = '<p>Checked modules are enabled.</p>\n'

	for module in SearchModule.loadedModules:
		modName = module.name
		moduleEnabledStr = ''
		if modName in configOptions['enabledModules']:
			moduleEnabledStr = ' checked="checked"'
		modulesHTML = modulesHTML + '<h3><input type="checkbox"' + moduleEnabledStr + '" name="modules" id="' + modName + '" value="' + modName + '" /><label for="' + modName + '">' + modName + '</label></h3>'
		moduleConfigHTML = module.configurationHTML()
		if len(moduleConfigHTML) > 0:
			modulesHTML = modulesHTML + '<fieldset id="' + modName + '-options" class="module-options">' + moduleConfigHTML + '</fieldset>'
	
	return render_template('config.html',configOptions=configOptions,optionNames=optionNames,modulesHTML=modulesHTML)

# Read the config file and return the HTML page
def config_read():
	cf = read_conf()
	webbuf_body = html_output(cf)
	return webbuf_body

# Write HTTP POST data to the config file
def config_write(request_form):
	cf = write_conf(request_form)

if __name__ == "__main__":
	#~ debug
	cf = read_conf()
	print cf

	webbuf_ret = html_output(cf)
	
	myFile = open('results.html', 'w')
	myFile.write(webbuf_ret)
	myFile.close()

