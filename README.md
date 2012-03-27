iett maps
---------

This is source code for [maps.yilmazhuseyin.com](http://maps.yilmazhuseyin.com).

Requirements
------------
* python3.2
* mongodb
* cherrypy
* jinja2
* pymongo3

Deployment
----------

  Project uses the result data for [iett-crawler](https://github.com/huseyinyilmaz/iett-crawler). Already generated data can be found [here](http://cdn.yilmazhuseyin.com/data/iettbus.tar.gz). Untar given file. There will be iettbus.json file inside. Copy this file into root directory of the project and run 

    python load_data.py

After this run

    python.server.py

To run the project. If you need to change database connection variables etc. You can do it from settings.py file.

