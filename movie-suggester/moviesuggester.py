  
# Patryk Kośmider s16863
# Krzysztof Marek s16663
# 
# Movie Suggester

import json
from compute_scores import euclidean_score, pearson_score

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
best = [ 0, '' ]
worst = [ 0, '' ]

with open('result.txt', 'w', encoding = 'utf-8') as file:
    file.write(f'Data for user {user}\n')

    for respondent in dataset:
        if user == respondent:
            continue

        ps_score = round(pearson_score(dataset, user, respondent), 2)

        # No correlation
        if ps_score == 0:
            file.write(f'\n[0] No correlation with {respondent}\n')
            continue

        eu_score = round(euclidean_score(dataset, user, respondent), 2)

        # Positive correlation
        if ps_score > 0:
            if eu_score * ps_score > best[0]:
                best[0] = ps_score
                best[1] = respondent
            
            file.write(f'\n[+] {get_positive_strength(ps_score)} correlation with {respondent}\n')

            common = get_common_movies(dataset, respondent, user)

            file.write(f'\tYou both tend to like:\n')
            for movie in common:
                m1 = dataset[respondent][movie]
                m2 = dataset[user][movie]
                if m1 > 5 and m2 > 5:
                    file.write(f'\t\t- "{movie}"\n')

            file.write(f'\tYou both tend to dislike:\n')
            for movie in common:
                m1 = dataset[respondent][movie]
                m2 = dataset[user][movie]
                if m1 < 5 and m2 < 5:
                    file.write(f'\t\t- "{movie}"\n')

            different = get_different_movies(dataset, respondent, user)

            file.write(f'\tI suggest you to watch:\n')
            for movie in different:
                if dataset[respondent][movie] * eu_score > 2:
                    file.write(f'\t\t- "{movie}"\n')
                
        # Negative correlation
        elif ps_score < 0:
            if eu_score * ps_score < worst[0]:
                worst[0] = ps_score
                worst[1] = respondent

            file.write(f'\n[-] {get_negative_strength(ps_score)} correlation with {respondent}\n')

            common = get_common_movies(dataset, respondent, user)

            file.write(f'\tYou both tend to disagree on:\n')
            for movie in common:
                m1 = dataset[respondent][movie]
                m2 = dataset[user][movie]
                if abs(m1 - m2) > 4:
                    file.write(f'\t\t- "{movie}"\n')

            different = get_different_movies(dataset, respondent, user)

            file.write(f'\tYou probably should not watch:\n')
            for movie in different:
                if dataset[respondent][movie] * eu_score > 1:
                    file.write(f'\t\t- "{movie}"\n')
            
            file.write(f'\tYou may like to watch:\n')
            for movie in different:
                if dataset[respondent][movie] * eu_score < 0.5:
                    file.write(f'\t\t- "{movie}"\n')
            
    file.write(f'\nBest match: {best[1]}\n')
    file.write(f'Worst match: {worst[1]}\n')
