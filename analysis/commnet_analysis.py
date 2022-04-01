from database import crud_comment_data
from values import constant


def analyse_proof_participation_comments_username_recurrence(table, order):

    if table == 'proof':
        table_name = constant.TABLE_NAME_COMMENT_PAGE_PROOF
    elif table == 'participation':
        table_name = constant.TABLE_NAME_COMMENT_PAGE_PARTICIPATION
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
