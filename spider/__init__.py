import requests
import bs4
from collections import Counter
import unidecode
from xml.dom import minidom
from main.models import Bus
import settings
import os

BUS_LIST_URL = 'http://harita.iett.gov.tr/'
#'http://www.iett.gov.tr/ajaxh_kodu.php?getCountriesByLetters=1&letters='

BUSSTOP_LIST_URL = \
    os.path.join(settings.XML_FILES, "%shatDurak.xml")

def get_bus_list():
    res = requests.post(BUS_LIST_URL)
    # result of the function
    result = []
    if res.ok:
        bs = bs4.BeautifulSoup(res.text)
        for op in bs.find(id='hat').findAll('option'):
            code = op.get('value')
            if code == '0':
                continue
            no, route = op.text.split(' - ', 1)
            result.append({'code': code,
                           'no': no,
                           'route': route,
                           'busstops': []})
    return result

def get_bus_list_old():
    """
    gets bus list from BUSLIST_URL
    and returns list of bus objects
    """
    res = requests.post(BUS_LIST_URL)
    # result of the function
    result = []
    # checking if we are getting same bus code twice
    # unicode conversation might screw buses up
    c = Counter()
    if res.ok:
        # loop list row by row
        # <b>bus # </b>:Bus route
        for row in filter(lambda x: x, res.text.split('|')):
            raw_no, route = row.strip().split(':')
            # remove b tags
            no = bs4.BeautifulSoup(raw_no).b.string
            # remove turkish chars for code
            code = unidecode.unidecode(no)
            # add busstop to result list
            result.append({'code': code, 'no': no, 'route': route})
            # increase counter
            c[code] += 1

    if not result:
        raise Exception('Could not retreive data')

    mc_code, mc_count = c.most_common(1)[0]
    if mc_count > 1:
        raise Exception('Duplicate bus codes [%s]' % mc_code)

    return result


def get_busstop_list(bus):
    no = bus['code'].lower()
    bs = bs4.BeautifulSoup(open(BUSSTOP_LIST_URL % no))
    result = []
    for item in bs.findAll('item'):
        busstop = {
            'title': item.title.text,
            'long': item.find('geo:long').text,
            'lat': item.find('geo:lat').text,
            'descrition': item.description.text,
            }
        result.append(busstop)

    return result


def pull_data():
    db = settings.db
    bus_collection = db[Bus._collection]

    bus_list = get_bus_list()
    online_set = set(map(lambda x: x['code'], bus_list))
    db_set = set(map(lambda x: x['code'], db.bus.find({}, {'code': 1})))

    s_diff = online_set.difference(db_set)
    if s_diff:
        bus_collection.insert(filter(lambda x: x['code'] in s_diff, bus_list))

    print('Current bus count is %s' % bus_collection.count())

    for bus in list(bus_collection.find()):
        try:
            bus['busstops'] = get_busstop_list(bus)
            bus_collection.save(bus)
        except IOError as e:
            bus_collection.remove(bus)
            print(e)

    for i in bus_collection.find({'busstops': {'$size': 0}}):
        bus_collection.remove(i)
