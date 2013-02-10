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

from flask import Flask
from flask import request

import SearchModule
import megasearch
import config_settings

app = Flask(__name__)
SearchModule.loadSearchModules()

@app.route('/s', methods=['GET'])
def search():
	cfg = config_settings.read_conf()
	if 'sortkey' in request.args:
		sortkey = request.args['sortkey']
	else:
		sortkey = 'relevance'
	
	if 'sortdir' in request.args:
		sortdir = request.args['sortdir']
	else:
		sortdir = 'asc'
	
	return megasearch.dosearch(request.args['q'], cfg, sortkey, sortdir)

@app.route('/config', methods=['GET','POST'])
def config():
	if request.method == 'POST':
		config_settings.config_write(request.form)
	return config_settings.config_read()
			
@app.route('/', methods=['GET','POST'])
def main_index():
	if request.method == 'POST':
		config_settings.config_write(request.form)
	cfg = config_settings.read_conf()
	if cfg['firstRun'] == '1':
		return config_settings.config_read()
	return megasearch.dosearch('', cfg)

@app.errorhandler(404)
def generic_error(error):
	return main_index()
	
if __name__ == "__main__":
	cfg = config_settings.read_conf()
	chost = cfg['host']
	cport = int(cfg['port'])
	app.run(host=chost,port=cport)
