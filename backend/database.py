### This file will manage users and aggregate data.
from numpy import genfromtxt
import json
import foursquare_api
import os

locations_to_rate_file = "locations_to_rate.csv"
profile_file = "profile.csv"
ratings_file = "ratings.csv"

userlist_file = "data/users/userlist.json"
venuelist_file = "data/venues/venuelist.json"

venue_data_file = "info.json"


# list of [place_id, name, date_of_visit, photo_url, description, location]
def get_user_locations_to_rate(user_id):
    with open("data/"+str(user_id)+"/"+locations_to_rate_file) as file:
        return json.load(file)

# list of [category_id, rating, confidence]
def get_user_profile(user_id):
    with open("data/"+str(user_id)+"/"+profile_file) as file:
        return json.load(file)

# list of [place_id, rating, confidence, tov => [time_of_visits]]
def get_user_ratings(user_id):
    with open("data/"+str(user_id)+"/"+ratings_file) as file:
        return json.load(file)

def get_userlist():
    with open(userlist_file) as file:
        return json.load(file)

# dict user -> user_profile
def get_profiles():
    users = get_userlist()
    result = {}
    for user in users:
        result[user] = get_user_profile(user)
    return result

# dict user -> user_ratings
def get_ratings():
    users = get_userlist()
    result = {}
    for user in users:
        result[user] = get_user_ratings(user)
    return result

def get_venuelist():
    with open(venuelist_file) as file:
        return json.load(file)

def get_venues_data():
    venues = get_venuelist()
    result = {}
    for venue in venues:
        result[venue] = get_venue_data(venue)
    return result

# list of [place_id, name, photo, description, longitude, latitude, [categories]]
def get_venue_data(venue_ID):
    try:
        with open("data/venues/"+str(venue_ID)+"/"+venue_data_file, "r") as read_file:
            data = json.load(read_file)
            return data
    except OSError as _: # venue info isn't cached yet
        # gather data from foursquare.
        details = foursquare_api.get_venue_details(venue_ID)
        photo_url = details["bestPhoto"]["prefix"] + "300x500" + details["bestPhoto"]["suffix"]
        
        categories_list = []
        for cat in details["categories"]:
            categories_list.append(cat["id"])
        
        info = {
            "name": details["name"],
            "photo": photo_url,
            "description": details["description"],
            "longitude": details["location"]["lng"],
            "latitude": details["location"]["lat"],
            "categories": categories_list
        }

        write_venue_data(venue_ID, info)


def write_venue_data(venue_ID, venue_data):
    filename = "data/venues/"+str(venue_ID)+"/"+venue_data_file
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    with open(filename, "w") as write_file:
        json.dump(venue_data, write_file)
