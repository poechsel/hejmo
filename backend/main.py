from flask import Flask
app = Flask(__name__)
import json
import database as db
import recommendation_system
import foursquare_api
import numpy as np

'''
Get vector profile of an user.
{
    cat_N: {
        rating: float;
        confidence: float;
    }
}
'''
@app.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    return json.dumps(db.get_user_profile(user_id))

'''
Get profile summary of an user.
{
    cat_N: {
        display_name: string;
        icon_url: string;
        interest: float;
    }
}
'''
@app.route('/profile_summary/<int:user_id>', methods=['GET'])
def get_profile_summary(user_id):
    user_profile = db.get_user_profile(user_id)
    score_category = [(value["rating"]*value["confidence"], key) for key, value in user_profile.items()]
    list.sort(score_category, reverse=True)
    response_data = []
    for score, category in score_category[:5]:
        display_name = foursquare_api.get_category_display_name(category)
        icon_url = foursquare_api.get_category_icon_url(category)
        response_data.append({
            "category_id": category,
            "display_name": display_name,
            "icon_url": icon_url,
            "interest": score
        })
    return json.dumps(response_data)



'''
Get a list of locations for the user to rate.
Returns
{
    Place_id
    Name
    Date of visit
    Photo
    Description
    Location
}
'''
@app.route('/locations_to_rate/<int:user_id>', methods=['GET'])
def get_locations_to_rate(user_id):
    user_data = db.get_user_locations_to_rate(user_id)
    
    user_profile = db.get_user_profile(user_id)
    questions_to_ask, category_level = recommendation_system.find_questions_to_ask(user_profile)
    
    output_places = []
    for entry in user_data:
        output_places.append({
            "place_id": entry[0],
            "name": entry[1],
            "date_of_visit": entry[2],
            "photo_url": entry[3],
            "description": entry[4],
            "location": entry[5]
        })

    output_categories = []
    for category in questions_to_ask:
        output_categories.append({
            "place_id": "+"+category,
            "name": foursquare_api.get_category_display_name(category) + " ?",
            "date_of_visit": 0,
            "photo_url": foursquare_api.get_category_icon_url(category),
            "description": "Are you interested in this category ?",
            "location": ""
        })

    if category_level == 1:
        question_probability = 0.5
    else:
        question_probability = 0.25

    output = []
    for _ in range(30):
        if np.random.random() < question_probability and len(output_categories) > 0:
            output.append(output_categories[0])
            output_categories = output_categories[1:]
        elif len(output_places) > 0:
            output.append(output_places[0])
            output_places = output_places[1:]
    return json.dumps(output)


'''
Get rated locations of an user.
{
    place_id: {
        rating: float;
        confidence_level: float;
        visits: [float];
    }
}
'''
@app.route('/locations/<int:user_id>', methods=['GET'])
def get_locations(user_id):
    return json.dumps(db.get_user_ratings(user_id))


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
@app.route('/recommendations/<int:user_id>/<category>/<float:lng>/<float:lat>/<int:time>', methods=['GET'])
def get_recommendations(user_id, category, lng, lat, time):
    users_profiles = db.get_profiles()
    users_rating = db.get_ratings()
    places = db.get_venues_data()
    results = recommendation_system.recommend_me_something_please(
        users_profiles, users_rating, places, user_id, category, time, lng, lat)
    
    output = []
    for res in results[:10]:
        output.append({
            "place_id": res["PID"],
            "matching_info": {
                "matched_people_score": res["score"]
            },
            "tip": ""
        })
    return json.dumps({"recommendations": output})

'''
Register a location with a rating, time of visit and an optional POST comment.
'''
@app.route('/put_location/<int:user_id>/<place_id>/<float:rating>/<int:time_of_visit>/')
def put_location(user_id, place_id, rating, time_of_visit):
    if place_id[0] == '+':
        put_affinity(user_id, place_id[1:], rating)

    one_day = 24*3600
    time_of_visit = time_of_visit % one_day

    # Update user ratings
    user_ratings = db.get_user_ratings(user_id)
    if place_id in user_ratings:
        user_ratings[place_id]["rating"], user_ratings[place_id]["confidence"] = recommendation_system.update_rating_flat(
            user_ratings[place_id]["rating"], user_ratings[place_id]["confidence"], rating)
        user_ratings[place_id]["visits"].append(time_of_visit)
    else:
        user_ratings[place_id] = {}
        user_ratings[place_id]["rating"] = rating
        user_ratings[place_id]["confidence"] = 1.0
        user_ratings[place_id]["visits"] = [time_of_visit]
    
    user_profile = db.get_user_profile(user_id)
    place_categories = db.get_venue_data(place_id)["categories"]
    for category in place_categories:
        user_profile[category]["rating"], user_profile[category]["confidence"] = (
            recommendation_system.update_rating_flat(
                user_profile[category]["rating"], user_profile[category]["confidence"], rating)
        ) 
    db.flush_user_ratings(user_id, user_ratings)
    db.flush_user_profile(user_id, user_profile)
    return "OK"


'''
Set category affinity.
'''
@app.route('/put_affinity/<int:user_id>/<category>/<float:affinity>/')
def put_affinity(user_id, category, affinity):
    user_profile = db.get_user_profile(user_id)
    user_profile[category]["rating"], user_profile[category]["confidence"] = (
        recommendation_system.update_rating_flat(
            user_profile[category]["rating"], user_profile[category]["confidence"], affinity)
    )
    db.flush_user_profile(user_id, user_profile)
    return "OK"
