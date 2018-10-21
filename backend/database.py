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
    with open(os.path.join(os.path.dirname(__file__), "data/users/"+str(user_id)+"/"+locations_to_rate_file)) as file:
        return json.load(file)

# list of [category_id, rating, confidence]
def get_user_profile(user_id):
    with open(os.path.join(os.path.dirname(__file__), "data/users/"+str(user_id)+"/"+profile_file)) as file:
        return json.load(file)

def flush_user_profile(user_id, data):
    with open(os.path.join(os.path.dirname(__file__), "data/users/"+str(user_id)+"/"+profile_file), "w") as file:
        json.dump(data, file)

# list of [place_id, rating, confidence, tov => [time_of_visits]]
def get_user_ratings(user_id):
    with open(os.path.join(os.path.dirname(__file__), "data/users/"+str(user_id)+"/"+ratings_file)) as file:
        return json.load(file)

def flush_user_ratings(user_id, data):
    with open(os.path.join(os.path.dirname(__file__), "data/users/"+str(user_id)+"/"+ratings_file), "w") as file:
        json.dump(data, file)


def get_userlist():
    with open(os.path.join(os.path.dirname(__file__), userlist_file)) as file:
        return json.load(file)


def add_to_userlist(id):
    with open(os.path.join(os.path.dirname(__file__), userlist_file), "r+") as file:
        data = json.load(file)
        data.append(id)
        file.seek(0)
        json.dump(data, file)
        file.truncate()

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
        with open(os.path.join(os.path.dirname(__file__), "data/venues/"+str(venue_ID)+"/"+venue_data_file), "r") as read_file:
            data = json.load(read_file)
            return data
    except OSError as _: # venue info isn't cached yet
        # gather data from foursquare.
        details = foursquare_api.get_venue_details(venue_ID)["venue"]
        if "bestPhoto" in details:
            photo_url = details["bestPhoto"]["prefix"] + "300x500" + details["bestPhoto"]["suffix"]
        else:
            photo_url = ""
        
        categories_list = []
        for cat in details["categories"]:
            categories_list.append(cat["id"])
        
        info = {
            "name": details["name"],
            "photo": photo_url,
            "description": "" if not("description" in details) else details["description"],
            "longitude": details["location"]["lng"],
            "latitude": details["location"]["lat"],
            "categories": categories_list
        }

        write_venue_data(venue_ID, info)
        return info


def write_venue_data(venue_ID, venue_data):
    filename = "data/venues/"+str(venue_ID)+"/"+venue_data_file
    if not os.path.exists(os.path.join(os.path.dirname(__file__), os.path.dirname(filename))):
        os.makedirs(os.path.join(os.path.dirname(__file__), os.path.dirname(filename)))

    with open(os.path.join(os.path.dirname(__file__), filename), "w+") as write_file:
        json.dump(venue_data, write_file)

def create_user():
    userlist = get_userlist()
    if len(userlist) == 0:
        new_id = 0
    else:
        new_id = max(userlist) + 1
    
    if not os.path.exists(os.path.join(os.path.dirname(__file__), os.path.dirname("data/users/"+str(new_id)+"/"))):
        os.makedirs(os.path.join(os.path.dirname(__file__), os.path.dirname("data/users/"+str(new_id)+"/")))
    
    with open(os.path.join(os.path.dirname(__file__), "data/users/"+str(new_id)+"/"+locations_to_rate_file), "w+") as f:
        f.write("[]")
    with open(os.path.join(os.path.dirname(__file__), "data/users/"+str(new_id)+"/"+profile_file), "w+") as f:
        categories_json_file = open(os.path.join(os.path.dirname(__file__), "data/categories.json"))
        categories = json.load(categories_json_file)

        data = {}
        to_explore = categories["categories"]
        while to_explore:
            cat = to_explore.pop()
            data[cat["id"]] = {
                "rating": 0.5,
                "confidence": 0.0
            }

            to_explore.extend(cat["categories"])
        
        json.dump(data, f)
    
    with open(os.path.join(os.path.dirname(__file__), "data/users/"+str(new_id)+"/"+ratings_file), "w+") as f:
        f.write("{}")
    
    add_to_userlist(new_id)
    return new_id
    