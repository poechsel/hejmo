import foursquare_api
import json

path = "backend/raw_profiles.txt"
file = open(path)
current = {"events": []}
profiles = []
for line in file.readlines():
    line = line.strip()
    if line == "":
        profiles.append(current)
        current = {"events": []}
    else:
        name, _, like, lat, lng = map(lambda x: x.strip(), line.split(","))
        venue = foursquare_api.get_venue_ID(lat, lng)
        print(name, venue["name"])
        current['events'].append({"venue": venue, "like": True if like == "aime" else False})

profiles.append(current)
print(profiles)
out_json = json.dumps(profiles)
out = open("profiles.json", "w")
out.write(out_json)


