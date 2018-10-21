### This file will contain the recommendation model.

import numpy as np
import utils

import foursquare_api

## User data structure
# users[id][category_id] = [rating, confidence_level]

## User visits data structure
# users_visits[id][place_id] = [time_of_visit, time_of_visit_spread, rating, confidence_level]

## Places data structure
# places[place_id] = [categories, lon, lat]


# check if request is a subcategory of parent.
def is_subcategory_of(request, parent):
    return foursquare_api.is_subcategory_of(request, parent)

def has_subcategory_of(request, parent):
    for cat in request:
        if is_subcategory_of(cat, parent):
            return True
    return False

# get subcategories of 
def get_subcategories_of(category):
    return foursquare_api.get_subcategories_of(category)

## Update rating and confidence for a flat measure (value between zero and one)
def update_rating_flat(current_rating, current_confidence_level, rating):
    new_rating = current_rating * current_confidence_level + rating * (1 - current_confidence_level)
    
    error = np.abs(new_rating - rating)
    new_confidence = max(0, current_confidence_level + (0.5 - error)*(1 - current_confidence_level))
    return new_rating, new_confidence

## Distance for flat rating.
def flat_ratings_distance(r1, r2):
    return np.abs(r1 - r2)

## Generic distance measure (scalar product) weighted by confidence in ratings.
def distance_with_confidence(users_profiles, user1, user2, selected_categories=None, ratings_distance_fn=flat_ratings_distance):
    profile1 = users_profiles[user1]
    profile2 = users_profiles[user2]

    distance = 0
    normalizer = 0
    if selected_categories == None:
        for cat, _ in profile1.items():
            total_conf = profile1[cat]["confidence"]*profile2[cat]["confidence"]
            normalizer += total_conf
            distance += total_conf*ratings_distance_fn(profile1[cat]["rating"], profile2[cat]["rating"])
    else:
        for cat in selected_categories:
            total_conf = profile1[cat]["confidence"]*profile2[cat]["confidence"]
            normalizer += total_conf
            distance += total_conf*ratings_distance_fn(profile1[cat]["rating"], profile2[cat]["rating"])
    
    if normalizer == 0: # they can't even compare their tastes!
        return 1
    else:
        return distance/normalizer

## Input:
# users_visits: visit history data structure
# category: category of interest
# lon, lat: coordinates
## Output:
# list of ids of users that have recommendations for the selected category near coordinates.
def filter_by_location(users_visits, places, requested_category, lon, lat, max_distance=3000):
    output = []
    for uid, visits in users_visits.items():
        n_potential = 0
        for place_id, visit_data in visits.items():
            rating, confidence_level = visit_data["rating"], visit_data["confidence"]
            categories, lon2, lat2 = places[place_id]["categories"], places[place_id]["longitude"], places[place_id]["latitude"]
            if utils.gps_distance(lon, lat, lon2, lat2) < max_distance and has_subcategory_of(categories, requested_category):
                if rating*confidence_level >= 0.5:
                    n_potential += 1
        if n_potential > 0:
            output.append((n_potential, uid))
    list.sort(output, reverse=True)
    return [y for _,y in output]

## Input:
# users: user category profile
# user_list: users to consider
# target_category: match within specified subcategory
## Output:
# [(score, user_id)] by descending order.
def match_by_category(users_profiles, user_list, target_user, target_category):
    scores = []
    selected_categories = get_subcategories_of(target_category)
    for user in user_list:
        score_category = distance_with_confidence(users_profiles, user, target_user, selected_categories)
        score = distance_with_confidence(users_profiles, user, target_user)
        # Score is a mix of general compatibility and intra-category compatibility.
        scores.append((score_category*(score+1)/2, user))
    list.sort(scores, reverse=True)
    return scores

## Given a gaussian of center time, with given spread. 
## What's its value at target_time ?
# between 0 and 1
def get_time_value(visit_time, target_time):
    two_hours = 2*3600
    min_diff = min([np.abs(ti - target_time) for ti in visit_time])
    coef = np.exp(-(min_diff/two_hours)**2)
    return 0.5 + 0.5*coef

## At which point should we factor in a place this far away?
# between 0 and 1
# Gaussian decrease: @2500m score is divided by 2. 
#                    @4500m score is divided by 10. (possibility to tweak this/make it a parameter)
def get_distance_value(lon, lat, target_lon, target_lat):
    distance = utils.gps_distance(lon, lat, target_lon, target_lat)
    return np.exp(-(distance/3000)**2)

# negative vote when bad review is given.
def get_user_value(user_score, review, confidence):
    return user_score * 2*(review-0.5) * confidence

## Operate a voting simulation taking into account matching and adequacy of each place.
def vote_for_places(users_ratings, places, scores, target_category, target_time, target_lon, target_lat):
    tally = {}
    for score, user in scores:
        for place_id, data in users_ratings[user].items():
            visits = data["visits"]
            rating = data["rating"]
            confidence_level = data["confidence"]

            categories, lon, lat = places[place_id]["categories"], places[place_id]["longitude"], places[place_id]["latitude"]

            if has_subcategory_of(categories, target_category):
                place_interest_time = get_time_value(visits, target_time)
                place_interest_distance = get_distance_value(lon, lat, target_lon, target_lat)
                place_interest_user = get_user_value(score, rating, confidence_level)

                vote_value = place_interest_distance*place_interest_time*place_interest_user
                if place_id in tally:
                    tally[place_id] += vote_value
                else:
                    tally[place_id] = vote_value
    return tally

## Recommendation algorithm.
def recommend_me_something_please(users_profiles, users_ratings, places, target_user, target_category, target_time, target_lon, target_lat):
    interesting_users       = filter_by_location(users_ratings, places, target_category, target_lon, target_lat)
    print(interesting_users)
    scores_by_categories    = match_by_category(users_profiles, interesting_users, target_user, target_category)
    print(scores_by_categories[:10])
    votes = vote_for_places(users_ratings, places, scores_by_categories, target_category, target_time, target_lon, target_lat)
    place_id = [x for x,_ in votes.items()]
    value = [x for _,x in votes.items()]
    places_sorted = sorted(zip(value, place_id), reverse=True)
    result = []
    for score, place_id in places_sorted:
        if not(place_id in users_ratings[target_user]):
            result.append({"PID":place_id, "score": score})
    return result
