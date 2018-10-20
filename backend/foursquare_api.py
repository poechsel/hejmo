### Interface between this server and the Foursquare API. 
### Foursquare is useful to extract categories from locations.

import json, requests

categories_list_url = 'https://api.foursquare.com/v2/venues/categories'
venue_from_coordinates_url = 'https://api.foursquare.com/v2/venues/search'

app_id = "5OFFKXRXZNT1T2QURFRTEJGDLQ2UAUZRG2XVYAMDOIMNQEYL"
app_secret = "14OHZJOYESUQODBWU32V4NJYUM0UHO0IU4HZZW4F453LYJYI"

def get_venue_ID(latitude, longitude):
    params = dict(
        client_id=app_id,
        client_secret=app_secret,
        ll='',
        intent='browse',
        radius='10',
        llAcc='100'
    )

def get_venue_details(venue_ID):
    params = dict(
        client_id=app_id,
        client_secret=app_secret,
    )


def get_venue_category(venue_ID):
