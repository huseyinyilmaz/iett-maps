import settings
import json

SOURCE_FILE = 'iettbus.json'


def pull_data():
    db = settings.db
    data = json.load(open(SOURCE_FILE))

    # Clear db
    db.location.drop()
    db.bus.drop()

#    db.location.insert(data['locations'])
    location_dict = dict(map(lambda x: (x['id'], x), data['locations']))

    def process_busstop(busstop):
        """
        Process busstops of busses.
        """
        location = location_dict[busstop['location_id']]
        busstop['long'] = location['long']
        busstop['lat'] = location['lat']

        del busstop['location_id']

        return busstop

    def process_bus(bus):
        bus['busstops'] = list(map(process_busstop, bus['busstops']))
        return bus

    buses = list(map(process_bus, data['buses']))

    db.bus.insert(buses)


if __name__ == '__main__':
    pull_data()
