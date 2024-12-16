from pandas import DataFrame

from apigame.database.db import UserDB

user_db = UserDB()


def authenticate_user(username, password):
    return user_db.check_user_credentials(username, password)


def get_user_by_username(username):
    return user_db.get_user_by_username(username)


def format_ranking_table(table):
    """
    Receives the ranking table with 'user_id' and 'points' columns and returns a new table
    where 'user_id' is replaced with the corresponding username.

    :param table: DataFrame with columns ['user_id', 'points']
    :return: Updated DataFrame with columns ['username', 'points']
    """
    updated_rows = []

    for _, row in table.iterrows():
        user_id = row['user_id']
        user_data = user_db.get_user_by_id(user_id)

        username = user_data.get('username', 'Unknown')

        updated_row = {
            'username': username,
            'points': row['points']
        }
        updated_rows.append(updated_row)

    # Convert the updated rows back into a DataFrame
    formatted_table = DataFrame(updated_rows, columns=['username', 'points'])
    return formatted_table
