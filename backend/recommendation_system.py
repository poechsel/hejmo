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
# target_category: match using only specified subcategory
## Output:
# [(score, user_id)] by descending order.
def match_by_category(users, places, user_list, target_user, target_category):
    scores = []
    selected_categories = get_subcategories_of(target_category)
    for user in user_list:
        ratings = users[selected_categories, 0]
        confidence_levels = users[selected_categories, 1]
        score = distance_with_confidence(ratings, confidence_levels, user, target_user)
        scores.append((score, user))
    list.sort(scores, reverse=True)
    return scores

## Operate a voting simulation taking into account matching and adequacy of each place.
def vote_for_places(users_visits, places, scores, target_category, target_time, target_lon, target_lat):
    tally = {}
    for score, user in scores:
        pass
    return tally

## Recommendation algorithm.
def recommend_me_something_please(users, users_visits, places, target_user, target_category, target_time, target_lon, target_lat):
    interesting_users = filter_by_location(users_visits, places, target_category, target_lon, target_lat)
    scores_by_categories = match_by_category(users, places, interesting_users, target_user, target_category)

