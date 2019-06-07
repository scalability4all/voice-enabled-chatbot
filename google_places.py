import requests
import json
from collections import namedtuple
import urllib
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))


def nearby_places(
        api_key,
        location,
        query,
        latitude,
        longitude,
        sort_by="prominence"):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    if "near" in query:
        sort_by = "distance"
    req = "{url}query='{query}'&location={latitude},{longitude}&rankby={rankby}&key={key}".format(
        url=url,
        query=query,
        latitude=latitude,
        longitude=longitude,
        key=api_key,
        rankby=sort_by
    )
    # print(req)
    r = requests.get(req)
    x = r.json()
    y = x['results']
    arr = []
    count = 5
    for i in range(min(count, len(y))):
        arr.append(y[i]['name'])
    return arr, y


def get_location():
    # {u'city': u'Hyderabad', u'longitude': 78.4744,
    # u'latitude': 17.3753, u'state': u'Telangana', u'IPv4': u'157.48.48.45',
    #  u'country_code': u'IN', u'country_name': u'India', u'postal': u'500025'}
    url = "https://geoip-db.com/json"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    data_named = namedtuple("User", data.keys())(*data.values())
    return data_named


def filter_sentence(text):
    word_tokens = word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if w not in stop_words]
    ans = ""
    for x in filtered_sentence:
        ans = ans + x + " "
    return ans


def change_location_query(address, key):
    url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(
        address, key)
    r = requests.get(url)
    x = r.json()
    user = namedtuple('User', 'city longitude latitude place_id')
    # print(x)
    try:
        x = x['results']
        location = x[0]['address_components'][2]['long_name']
        lattitude = x[0]['geometry']['location']['lat']
        longitude = x[0]['geometry']['location']['lng']
        return user(
            city=location,
            longitude=longitude,
            latitude=lattitude,
            place_id=x[0]['place_id'])
    except Exception as e:
        print(e)
        return user(
            city="Hyderabad",
            longitude=17.44,
            latitude=78.34,
            place_id="ChIJK_h_8QMKzjsRlrTemJvoAp0")
