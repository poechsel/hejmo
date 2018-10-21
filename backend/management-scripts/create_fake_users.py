import sys
sys.path.append("..")
import json
import database as db
import main

profiles_path = "fake_profiles.json"

with open(profiles_path, 'r') as file:
    content = json.load(file)
## Content format:
# [
# {
#   events: [
#       {
#        venue: {},
#        like: bool
#       }
#   ]
# }
# ]
 
for data in content:
    uid = db.create_user()
    for event in data["events"]:
        rating = 1.0 if event["like"] else 0.0
        main.put_location(uid, event["venue"]["id"], rating, 0)
 
