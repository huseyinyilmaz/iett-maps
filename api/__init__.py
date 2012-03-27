import cherrypy
import json


class BusHandler:
    def index(self):
        cherrypy.response.headers['Content-Type'] = 'text/json'
        return json.dumps(
            [{'code': bus['code'], 'no': bus['no']}
             for bus in cherrypy.db.bus.find({}, {'code': 1, 'no': 1})])

    index.exposed = True


class BusStopHandler:
    def index(self, route):
        cherrypy.response.headers['Content-Type'] = 'text/json'
        bus = cherrypy.db.bus.find_one({'code': route}, {'busstops': 1})
        return json.dumps({
                "type": "FeatureCollection",
                "features": [
                    {"type": "Feature",
                     "geometry": {
                            "type": "Point",
                            "coordinates": [busstop['long'], busstop['lat']]},
                     "properties": {"title": busstop['title']}}
                    for busstop in bus['busstops']]
                } if bus else {'error': 'Aradiginiz busstop bulunamadi'})

    index.exposed = True
