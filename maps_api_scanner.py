import requests
import warnings
import json
import colorama
from functools import reduce
from operator import getitem


colorama.init()


def good(msg):
    print("{}{}{}\n".format(colorama.Fore.GREEN, msg, colorama.Style.RESET_ALL))


def bad(msg):
    print("{}{}{}\n".format(colorama.Fore.RED, msg, colorama.Style.RESET_ALL))


def meh(msg):
    print("{}{}{}\n".format(colorama.Fore.BLUE, msg, colorama.Style.RESET_ALL))


def get_nested_item(data, keys):
    return reduce(getitem, keys, data)


def get_error(resp, keys):
    error = ""
    try:
        response = resp.json()
        try:
            error = get_nested_item(response, keys)
        except TypeError:
            pass
    except ValueError:
        error = resp.content.decode("utf-8")
    return error


warnings.filterwarnings("ignore")
apikey = input("Please enter the Google Maps API key you wanted to test: ")
apis = {
    "Staticmap API": {
        "url": "https://maps.googleapis.com/maps/api/staticmap?center=45%2C10&zoom=7&size=400x400&key={}",
        "poc": "{}",
    },
    "Streetview API": {
        "url": "https://maps.googleapis.com/maps/api/streetview?size=400x400&location=40.720032,-73.988354&fov=90&heading=235&pitch=10&key={}",
        "poc": "{}",
    },
    "Embed API": {
        "url": "https://www.google.com/maps/embed/v1/place?q=place_id:ChIJyX7muQw8tokR2Vf5WBBk1iQ&key=",
        "poc": '<iframe width="600" height="450" frameborder="0" style="border:0" src="{}" allowfullscreen></iframe>',
    },
    "Directions API": {
        "url": "https://maps.googleapis.com/maps/api/directions/json?origin=Disneyland&destination=Universal+Studios+Hollywood4&key={}",
        "poc": "{}",
        "error": ["error_message"],
    },
    "Geocode API": {
        "url": "https://maps.googleapis.com/maps/api/geocode/json?latlng=40,30&key={}",
        "poc": "{}",
        "error": ["error_message"],
    },
    "Distance Matrix API": {
        "url": "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=40.6655101,-73.89188969999998&destinations=40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.659569%2C-73.933783%7C40.729029%2C-73.851524%7C40.6860072%2C-73.6334271%7C40.598566%2C-73.7527626%7C40.659569%2C-73.933783%7C40.729029%2C-73.851524%7C40.6860072%2C-73.6334271%7C40.598566%2C-73.7527626&key={}",
        "poc": "{}",
        "error": ["error_message"],
    },
    "Find Place From Text API": {
        "url": "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Museum%20of%20Contemporary%20Art%20Australia&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key={}",
        "poc": "{}",
        "error": ["error_message"],
    },
    "Autocomplete API": {
        "url": "https://maps.googleapis.com/maps/api/place/autocomplete/json?input=Bingh&types=%28cities%29&key={}",
        "poc": "{}",
        "error": ["error_message"],
    },
    "Elevation API": {
        "url": "https://maps.googleapis.com/maps/api/elevation/json?locations=39.7391536,-104.9847034&key={}",
        "poc": "{}",
        "error": ["error_message"],
    },
    "Timezone API": {
        "url": "https://maps.googleapis.com/maps/api/timezone/json?location=39.6034810,-119.6822510&timestamp=1331161200&key={}",
        "poc": "{}",
        "error": ["errorMessage"],
    },
    "Roads API": {
        "url": "https://roads.googleapis.com/v1/nearestRoads?points=60.170880,24.942795|60.170879,24.942796|60.170877,24.942796&key={}",
        "poc": "{}",
        "error": ["error", "message"],
    },
    "Geolocation API": {
        "url": "https://www.googleapis.com/geolocation/v1/geolocate?key={}",
        "poc": "curl -i -s -k  -X $'POST' -H $'Host: www.googleapis.com' -H $'Content-Length: 22' --data-binary $'{\"considerIp\": \"true\"}' $'{}'",
        "data": {"considerIp": "true"},
        "error": ["error", "message"],
    },
}
for api, info in apis.items():
    url = info["url"].format(apikey)
    error = ""
    if "data" in info:
        resp = requests.post(url, data=info["data"])
    else:
        resp = requests.get(url)
    if resp.ok:
        if "error" in info:
            error = get_error(resp, info["error"])
        else:
            bad(
                "API Key is vulnerable to the {}. Below is a Proof of Concept:\n{}".format(
                    api, info["poc"].format(url)
                )
            )
    else:
        error = get_error(resp, info.get("error", []))
    if error:
        good("Key is not vulnerable to the {}. Reason:\n{}".format(api, error))

meh(
    "Because JavaScript API needs manual confirmation from a web browser, tests are not conducted for that API. If the script didn't found any vulnerable endpoints above, to be sure, manual checks can be conducted on this API. For that, go to https://developers.google.com/maps/documentation/javascript/tutorial URL, copy HTML code and change 'key' parameter with the one wanted to test. If loaded without errors on the browser, then it is vulnerable for JavaScript API."
)
