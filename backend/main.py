from flask import Flask
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
@app.route('/get_profile/<int:user_id>')
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
@app.route('/get_locations_to_rate/<int:user_id>')
def get_locations_to_rate(user_id):
    user_data = database.get_user_locations_to_rate(user_id)
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
@app.route('/get_locations/<int:user_id>')
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
@app.route('/get_recommendations/<int:user_id>/<int:category>/<float:location_x>/<float:location_y>/<int:time>/')
def get_recommendations(user_id, category, location_x, location_y, time):
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