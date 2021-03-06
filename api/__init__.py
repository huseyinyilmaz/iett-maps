import cherrypy
import json


class BusHandler:
    def index(self):
        cherrypy.response.headers['Content-Type'] = 'text/json'

        return json.dumps(
            [{'code': bus['code'], 'no': bus['no'], 'route': bus['route']}
             for bus in cherrypy.db.values()])

    index.exposed = True


class BusStopHandler:
    def index(self, route):
        cherrypy.response.headers['Content-Type'] = 'text/json'
        bus = cherrypy.db[route]
        return json.dumps({
            "type": "FeatureCollection",
            "features": [
                {"type": "Feature",
                 "geometry": {
                     "type": "Point",
                     "coordinates": [busstop['long'], busstop['lat']]},
                 "properties": {"title": busstop['title']}}
                for busstop in bus['busstops']]}
            if bus else {'error': 'Aradiginiz busstop bulunamadi'})

    index.exposed = True
