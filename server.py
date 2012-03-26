#! python
"""
Tutorial - Passing variables

This tutorial shows you how to pass GET/POST variables to methods.
"""

import cherrypy
import main
import settings
import api


root = main.Root()


class Api:
    bus = api.BusHandler()
    busstop = api.BusStopHandler()
root.api = Api()


cherrypy.db = settings.db

cherrypy.templates = settings.templates

if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    cherrypy.quickstart(root, config=settings.conf)
else:
    # This branch is for the test suite; you can ignore it.
    #cherrypy.tree.mount(WelcomePage(), config=tutconf)
    pass
