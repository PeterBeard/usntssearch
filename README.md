**NZBmegasearcH** 
======================

NZBmegasearcH is a program that collects all your newznab (and many others) accounts to one place.   
Are you tired to search by using many different sites (nzb.cc, omgwtfnzbs, nzb.su etc)? Well, that's the solution for you. NZBmegasearcH aggregates search results from all your accounts in one clean web interface.

Technically speaking: NZBmegasearcH is a meta-search engine that retreives data from your favourite NZB indices.

=======
That's more: you can configure to use it with your SB and CP as a unique provider.

*Features*:
* Support for accounts from any Newsnb and Spotweb based provider
* Support for web-only access to Newsnb websites (in case API is not active)
* Support for nzb.cc, findnzb.info, ftdworld.net, wombie, omgwtfnzbs, gingadaddy and many others
* Support for CP, SB, NZB360, SABNZBD, NZBGET
* Detects PREDB releases
* Support for many search categories
* Retreives trending movies and shows
* Gives appropriate search suggestions
* Really small memory and CPU footprint
* SSH and user identification supported
>>>>>>> upstream/master

It is written in Python and it works on linux, mac, win. Windows binaries are also available.

**Latest version is 0.44**

This project makes use of:

- Python 2.7
- [Flask] (http://flask.pocoo.org/)
- [Requests] (http://docs.python-requests.org/en/latest/)
- [BeautifulSoup] (http://www.crummy.com/software/BeautifulSoup/)
- [Mechanize] (http://wwwsearch.sourceforge.net/mechanize/)
- [PyOpenSSL] (https://launchpad.net/pyopenssl/)

## Screenshots


* Configure  

![Config](https://raw.github.com/pillone/usntssearch/master/NZBmegasearch/static/show_config.jpg)

* Search  
![Search](https://raw.github.com/pillone/usntssearch/master/NZBmegasearch/static/show_search.jpg)
 

## [Install it for free and anonymously on the cloud](https://github.com/pillone/usntssearch/blob/master/NZBmegasearch/openshift/openshift_install.md)

 

## [Install it on your server (heavy traffic)](https://github.com/pillone/usntssearch/blob/master/NZBmegasearch/large_server/nginx_install.md)



## Install it on your computer

 

**Windows**

- Download latest available binary from [usntssearch-binaries/windows] (https://github.com/pillone/usntssearch-binaries/tree/master/windows)
- There are two binaries avaliable: 
 * [win32_NZBMegasearcH_0.XX-wconsole.zip] (https://github.com/pillone/usntssearch-binaries/raw/master/windows/win32_NZBMegasearcH_0.44-wconsole.zip) runs silently without console output
 * [win32_NZBMegasearcH_0.XX-noconsole.zip] (https://github.com/pillone/usntssearch-binaries/raw/master/windows/win32_NZBMegasearcH_0.44-noconsole.zip) runs with console output
- Unzip in a folder and click on `mega2.exe`
- Open browser to `localhost:5000`

**Linux**

- `apt-get install python2.7 git python-openssl`
- `git clone https://github.com/pillone/usntssearch.git`
- Enter in the usntssearch/NZBmegasearch directory and run  `python mega2.py` to start
- Open browser to `localhost:5000`


- Run in detached from terminal: `python mega2.py daemon`
- Autorun at reboot: add mega2.py in your crontab line with `@reboot`

## Updates


**Changes in v0.44**

- Bugfix obscure 500 error, thanks JackDandy
- Enhanced css, thanks JackDandy
- For so many bugfix and suggestions, thanks JackDandy :)
- Added manual IP option for SABNZB automation
- Added PREDB matching
- Added custom permanent search terms, suggestion by JackDandy

More updates are available in changelog.txt

<a title="website statistics" href="http://statcounter.com/" 
target="_blank"><img
src="http://c.statcounter.com/8769563/0/45111251/0/" alt="website statistics" style="border:none;"></a>

