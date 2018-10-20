from flask import Flask
app = Flask(__name__)
import json
import database as db


user_ratings = {}
user_profils = {}
locations_to_rate = {}
venues = {}
ratings = db.get_ratings()
profiles = db.get_profiles()
userlist = db.get_userlist()


'''
Get vector profile of an user.
{
    feature_vector: array[float];
}
'''
@app.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    return json.dumps(db.get_user_profile(user_id))



'''
Get a list of locations for the user to rate.
Returns
{
    Name
    Date of visit
    Photo
    Description
    Location
}
'''
@app.route('/locations_to_rate/<int:user_id>', methods=['GET'])
def get_locations_to_rate(user_id):
    user_data = db.get_locations_to_rate(user_id)
    output = []
    for entry in user_data:
        output.append({
            "place_id": entry[0],
            "name": entry[1],
            "date_of_visit": entry[2],
            "photo_ur": entry[3],
            "description": entry[4],
            "location": entry[5]
        })
    return json.dumps(output)


'''
Get rated locations of an user.
{
    place_id: int;
    rating: float;
    confidence_level: float;
    time_of_visit_mean: int;
    time_of_visit_spread: float;
}
'''
@app.route('/locations/<int:user_id>', methods=['GET'])
def get_locations(user_id):
    return db.get_user_ratings(user_id)


'''
Returns recommendations for an user.
{
    recommendations: array[{
        place_id: int;
        matching_info: {
            matched_people_score: float;
            group_category: int;
        };
        tip: string;
    }]
}
'''
@app.route('/recommendations/<int:user_id>/<int:category>/<float:lng>/<float:lat>/<int:time>/', methods=['GET'])
def get_recommendations(user_id, category, lng, lat, time):
    recommend_me_something_please(profiles, visits, venues,
                                  user_id, category, time, lng, lat)
    pass

'''
Register a location with a rating, time of visit and an optional POST comment.
'''
@app.route('/put_location/<int:user_id>/<int:place_id>/<float:rating>/<int:time_of_visit>/')
def put_location(user_id, place_id, rating, time_of_visit):
    pass

'''
Set category affinity.
'''
@app.route('/put_affinity/<int:user_id>/<int:category>/<float:affinity>/')
def put_affinity(user_id, category, affinity):
    pass
