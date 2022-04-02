from database import db_crud_comments
from values import constant


def analyse_proof_participation_comments_username_recurrence(table, order):

    if table == 'proof':
        table_name = constant.DB_PROOF
    elif table == 'participation':
        table_name = constant.DB_PARTICIPATION
    else:
        print('1st argument should be proof or participation')
        return

    username_recurrence_proof = crud_comment_data.retrieve_participation_proof_comments_username_recurrence(table_name)

    match order:
        case 'asc':
            sorted_by_username = sorted(username_recurrence_proof, key=lambda tup: tup[1])
        case 'desc':
            sorted_by_username = sorted(username_recurrence_proof, key=lambda tup: tup[1], reverse=True)

    return sorted_by_username

# IDEA: ANALYSE CAMPAIGNS COLUMN IN PROOF TABLE TO SEE MOST POPULAR SOCIAL MEDIA SOURCES
