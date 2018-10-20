from flask import Flask
import json
import recommandation_systems
app = Flask(__name__)
import json
import database as db



locations_to_rate = {}

@app.route('/')
def hello_world():
    return ''

'''
Get vector profile of an user.
{
    feature_vector: array[float];
}
'''
@app.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    pass



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
@app.route('/locations_to_rate/<int:user_id>', methods=["GET"])
def get_locations_to_rate(user_id):
    user_data = database.get_locations_to_rate(user_id)
    output = []
    for entry in user_data:
        output.append({
            "place_id": entry[0],
            "name": entry[1],
            "date_of_visit": entry[2],
            "photo_url": entry[3],
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
    pass


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
@app.route('/recommendations/<int:user_id>/<int:category>/<float:lat>/<float:lng>/<int:time>/', methods=['GET'])
def get_recommendations(user_id, category, lat, lng, time):
    recommandations = recommendation_systems.recommand_me_something(users, users_visits, places, user_id, category, time, lat, lng)
    return json.dumps(recommandations)
    
'''
Register a location with a rating, time of visit and an optional POST comment.
'''
@app.route('/location/<int:user_id>/<int:place_id>/<float:rating>/<int:time_of_visit>/', methods=['PUT'])
def put_location(user_id, place_id, rating, time_of_visit):
    pass

'''
Set category affinity.
'''
@app.route('/affinity/<int:user_id>/<int:category>/<float:affinity>/', methods=['PUT'])
def put_affinity(user_id, category, affinity):
    
