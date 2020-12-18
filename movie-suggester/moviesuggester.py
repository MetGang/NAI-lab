  
# Patryk Kośmider s16863
# Krzysztof Marek s16663
# 
# Movie Suggester

import json
from compute_scores import euclidean_score, pearson_score
from collections import OrderedDict

def get_common_movies(dataset, u1, u2):
    common = []

    for item in dataset[u1]:
        if item in dataset[u2]:
            common.append(item)

    return common

def get_different_movies(dataset, u1, u2):
    different = []

    for item in dataset[u1]:
        if item not in dataset[u2]:
            different.append(item)

    return different

def get_positive_strength(score):
    if score > 0.8:
        return 'Very positive'
    if score > 0.5:
        return 'Mostly positive'
    if score > 0.3:
        return 'Positive'
    return 'Slightly positive'

def get_negative_strength(score):
    if abs(score) > 0.8:
        return 'Very negative'
    if abs(score) > 0.5:
        return 'Mostly negative'
    if abs(score) > 0.3:
        return 'Negative'
    return 'Slightly negative'

with open('dataset.json', 'r', encoding = 'utf-8') as file:
    dataset = json.load(file)

user = input('Enter user name: ')

if user not in dataset:
    raise RuntimeError("User not found!")

to_remove = []

for respondent in dataset:
    #PS -> 1.0 = perfect correlation, -1.0 = reverse correlation, 0.0 = no correlation
    dataset[respondent]['ps_score'] = pearson_score(dataset, user, respondent)
    #EU -> 1.0 = perfect, 0.0 = imperfect, more = better, less = worse
    dataset[respondent]['eu_score'] = euclidean_score(dataset, user, respondent)
    if user == respondent:
        dataset[respondent]['ps_score'] = 0.0
        dataset[respondent]['eu_score'] = 0.0
    if dataset[respondent]['ps_score'] < 0.5:
        to_remove.append(respondent)
best_users = dataset.copy()
for respondent in to_remove:
    best_users.pop(respondent)
best_users = OrderedDict(sorted(best_users.items(), key=lambda item: item[1]['eu_score']))
best_movies = OrderedDict()
for respondent in best_users:
    for movie in best_users[respondent]:
        if movie == 'eu_score' or movie == 'ps_score' or movie in dataset[user]:
            continue
        if movie in best_movies:
            best_movies[movie] = [best_movies[movie][0] + best_users[respondent][movie] * best_users[respondent]['eu_score'], best_movies[movie][1] + 1]
        else:
            best_movies[movie] = [best_users[respondent][movie] * best_users[respondent]['eu_score'], 1]
for movie in best_movies:
    best_movies[movie][0] = best_movies[movie][0] / best_movies[movie][1]
best_movies = OrderedDict(sorted(best_movies.items(), key=lambda item: (item[1][1], item[1][0]), reverse=True))
i = 0
print('Movies you should watch:')
for movie in best_movies:
    print(movie)
    i = i + 1
    if i == 5:
        break
worst_movies = OrderedDict(sorted(best_movies.items(), key=lambda item: (item[1][0]), reverse=False))
i = 0
print('\nMovies you shouldn\'t watch:')
for movie in worst_movies:
    print(movie)
    i = i + 1
    if i == 5:
        break
