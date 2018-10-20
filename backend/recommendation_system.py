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
def distance_with_confidence(ratings, confidence_levels, user1, user2, ratings_distance_fn=flat_ratings_distance):
    normalizer = np.sum(confidence_levels[user1]*confidence_levels[user2])
    return np.sum(ratings_distance_fn(ratings[user1], ratings[user2])*confidence_levels[user1]*confidence_levels[user2])/normalizer


## Input:
# users_visits: visit history data structure
# category: category of interest
# lon, lat: coordinates
## Output:
# list of ids of users that have recommendations for the selected category near coordinates.
def filter_by_location(users_visits, places, requested_category, lon, lat, max_distance=3000):
    output = []

    for uid, visits in enumerate(users_visits):
        n_potential = 0
        for place_id, (_, _, rating, confidence_level) in enumerate(visits):
            categories, lon2, lat2 = places[place_id]
            if utils.gps_distance(lon, lat, lon2, lat2) < max_distance and is_subcategory_of(categories, requested_category):
                if rating*confidence_level >= 0.5:
                    n_potential += 1
        if n_potential > 0:
            output.append((n_potential, uid))
    list.sort(output, reverse=True)
    return zip(*output)[1]

## Input:
# users: user category profile
# places: places database
# user_list: users to consider
# target_category: match within specified subcategory
## Output:
# [(score, user_id)] by descending order.
def match_by_category(users, places, user_list, target_user, target_category):
    scores = []
    selected_categories = get_subcategories_of(target_category)
    for user in user_list:
        ratings = users[selected_categories, 0]
        confidence_levels = users[selected_categories, 1]
        score_category = distance_with_confidence(ratings, confidence_levels, user, target_user)
        score = distance_with_confidence(users[:, 0], users[:, 1], user, target_user)
        # Score is a mix of general compatibility and intra-category compatibility.
        scores.append((score_category*(score+1)/2, user))
    list.sort(scores, reverse=True)
    return scores

## Given a gaussian of center time, with given spread. 
## What's its value at target_time ?
# between 0 and 1
def get_time_value(time, spread, target_time):
    one_day = 24*3600
    tests = [time - target_time, time - one_day - target_time, time + one_day - target_time]

    coef = 0
    for test in tests:
        coef = np.max(coef, np.exp(-(test/spread)**2))
    return 0.5 + 0.5*coef

## At which point should we factor in a place this far away?
# between 0 and 1
# Gaussian decrease: @2500m score is divided by 2. 
#                    @4500m score is divided by 10. (possibility to tweak this/make it a parameter)
def get_distance_value(lon, lat, target_lon, target_lat):
    distance = utils.gps_distance(lon, lat, target_lon, target_lat)
    return np.exp(-(distance/3000)**2)

def get_user_value(user_score, review, confidence):
    return user_score * review * confidence

## Operate a voting simulation taking into account matching and adequacy of each place.
def vote_for_places(users_visits, places, scores, target_category, target_time, target_lon, target_lat):
    tally = {}
    for score, user in scores:
        for place_id, (time, spread, rating, confidence_level) in enumerate(users_visits[user]):
            category, lon, lat = places[place_id]
            if is_subcategory_of(category, target_category):
                place_interest_time = get_time_value(time, spread, target_time)
                place_interest_distance = get_distance_value(lon, lat, target_lon, target_lat)
                place_interest_user = get_user_value(score, rating, confidence_level)

                vote_value = place_interest_distance*place_interest_time*place_interest_user
                if place_id in tally:
                    tally[place_id] += vote_value
                else:
                    tally[place_id] = vote_value
    return tally

## Recommendation algorithm.
def recommend_me_something_please(users, users_visits, places, target_user, target_category, target_time, target_lon, target_lat):
    interesting_users       = filter_by_location(users_visits, places, target_category, target_lon, target_lat)
    scores_by_categories    = match_by_category(users, places, interesting_users, target_user, target_category)
    votes = vote_for_places(users_visits, places, scores_by_categories, target_category, target_time, target_lon, target_lat)
    place_id, value = zip(*votes.items())
    places_sorted = sorted(zip(value, place_id), reverse=True)
    result = []
    for _, place_id in places_sorted:
        if not(place_id in users_visits[target_user]):
            result.append(place_id)
    return result
