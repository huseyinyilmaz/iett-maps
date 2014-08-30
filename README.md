iett maps
---------

This is source code for [maps.yilmazhuseyin.com](http://maps.yilmazhuseyin.com).

Requirements
------------
* python 3
* cherrypy
* jinja2


Deployment
----------

  Project uses the result data for [iett-crawler](https://github.com/huseyinyilmaz/iett-crawler). Already generated data can be found [here](http://cdn.yilmazhuseyin.com/data/iettbus.tar.gz). Untar given file. There will be iettbus.json file inside. Copy this file into root directory of the project and run 

    python load_data.py

After this run

    python.server.py

 