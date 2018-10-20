### This file will contain the recommendation model.

import numpy as np


## User data structure
# users[id][category_id] = [rating, confidence_level]

## User visits data structure
# users[id][place_id] = [time_of_visit, time_of_visit_spread, rating, confidence_level]

## Places data structure
# places[place_id] = [categories, lon, lat]


def update_rating_flat(current_rating, current_confidence_level, rating):
    new_rating = current_rating * current_confidence_level + rating * (1 - current_confidence_level)
    
    error = np.abs(new_rating - rating)
    new_confidence = max(0, current_confidence_level + (0.5 - error)*(1 - current_confidence_level))
    return new_rating, new_confidence

def flat_ratings_distance(r1, r2):
    return np.abs(r1 - r2)

def distance_with_confidence(ratings, confidence_levels, user1, user2, ratings_distance_fn=flat_ratings_distance):
    normalizer = np.sum(confidence_levels[user1]*confidence_levels[user2])
    return np.sum(ratings_distance_fn(ratings[user1], ratings[user2])*confidence_levels[user1]*confidence_levels[user2])/normalizer
