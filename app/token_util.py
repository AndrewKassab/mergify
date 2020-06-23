import time
from db.database import db
from spotify import refresh_access_token


def is_users_access_token_expired(username):
    expiration_time = db.get_expiration_time_for_user(username)
    if time.time() > expiration_time:
        return True
    return False


def is_access_token_valid(access_token, username):
    actual_token = db.get_access_token_for_user(username)
    if access_token == actual_token:
        return True
    return False


def refresh_and_update_access_token_for_user(username):
    refresh_token = db.get_refresh_token_for_user(username)
    new_token = refresh_access_token(refresh_token)['access_token']
    db.update_access_token_for_user(username, new_token)
    return new_token

