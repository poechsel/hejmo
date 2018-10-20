### Interface between this server and the Foursquare API. 
### Foursquare is useful to extract categories from locations.

import foursquare
import auth.foursquare_secret as secret

categories_list_url = 'https://api.foursquare.com/v2/venues/categories'
venue_from_coordinates_url = 'https://api.foursquare.com/v2/venues/search'


client = foursquare.Foursquare(
    client_id=secret.id,
    client_secret=secret.secret,
    redirect_uri='http://fondu.com/oauth/authorize')
auth_uri = client.oauth.auth_url()

def get_venue_ID(latitude, longitude):
    params = dict(
        client_id=app_id,
        client_secret=app_secret,
        ll=','.join([str(latitude), str(longitude)]),
        intent='browse',
        radius='250',
        llAcc='100'
    )
    return client.venues.search(params)

def get_venue_details(venue_ID):
    return client.venues(venue_ID)


def get_venue_category(venue_ID):
    pass

# print(get_venue_details("412d2800f964a520df0c1fe3"))
