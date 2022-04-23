# IDEA: ANALYSE HOW MANY TOPICS ARE WRITTEN BY THE SAME USERS
from database import crud_analysis


def author_frequency(order):
    username_frequency = crud_analysis.read('topic[author_frequency]', [])

    match order:
        case 'asc':
            sorted_by_username = sorted(username_frequency, key=lambda tup: tup[1])
        case 'desc':
            sorted_by_username = sorted(username_frequency, key=lambda tup: tup[1], reverse=True)

    return sorted_by_username
