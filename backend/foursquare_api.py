### Interface between this server and the Foursquare API. 
### Foursquare is useful to extract categories from locations.

import foursquare
import json
import auth.foursquare_secret as secret
import os

categories_list_url = 'https://api.foursquare.com/v2/venues/categories'
venue_from_coordinates_url = 'https://api.foursquare.com/v2/venues/search'


categories_json_file = open(os.path.join(os.path.dirname(__file__), "data/categories.json"))
categories_json = categories_json_file.read()
categories = json.loads(categories_json)

import copy

category_map = {}

category_to_children = {}
category_to_parent = {}

def build_categorie_map(categories, parents=[], parent_id=""):
    category_to_children[parent_id] = []
    for category in categories:
        current = copy.deepcopy(category)
        current["categories"] = []
        path = parents + [current]
        category_map[category["id"]] = path
        build_categorie_map(category["categories"], path, current["id"])
        category_to_parent[category["id"]] = parent_id
        category_to_children[parent_id].append(category["id"])

def is_subcategory_of(request, parent):
    if request in category_to_parent:
        if category_to_parent[request] == parent:
            return True
        return is_subcategory_of(category_to_parent[request], parent)
    return False

def get_subcategories_of(category):
    return category_to_children.get(category, [])

build_categorie_map(categories["categories"])


client = foursquare.Foursquare(
    client_id=secret.id,
    client_secret=secret.secret,
    redirect_uri='http://fondu.com/oauth/authorize')
auth_uri = client.oauth.auth_url()

def get_venue_ID(latitude, longitude):
    params = dict(
        ll=','.join([str(latitude), str(longitude)]),
        intent='browse',
        radius='250',
        llAcc='100'
    )

    venues = client.venues.search(params)

    min_venue = min(venues["venues"], key = lambda venue : venue.get("distance", float("+inf")))

    categories_id = set()
    categories = []
    for cat in min_venue["categories"]:
        for parent in category_map[cat["id"]]:
            if not parent["id"] in categories_id:
                categories_id.add(parent["id"])
                categories.append(parent)
    min_venue["categories"] = categories
    return min_venue

def get_venue_details(venue_ID):
    return client.venues(venue_ID)


def get_venue_category(venue_ID):
    pass

# print(get_venue_ID( 52.235823, 21.000785))
#print(get_venue_details("412d2800f964a520df0c1fe3"))
#print(json.dumps(client.venues.categories()))
