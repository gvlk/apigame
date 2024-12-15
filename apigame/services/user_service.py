from apigame.database.db import UserDB

user_db = UserDB()


def authenticate_user(username, password):
    return user_db.check_user_credentials(username, password)


def get_user_by_username(username):
    return user_db.get_user_by_username(username)
