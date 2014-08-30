import settings
import json

SOURCE_FILE = 'iettbus.json'


def pull_data():
    db = settings.db
    data = json.load(open(SOURCE_FILE))

    # Clear db
    db.clear()

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
    buses = {bus['code']: bus for bus in map(process_bus, data['buses'])}
    db.update(buses)
    db.sync()


if __name__ == '__main__':
    pull_data()
