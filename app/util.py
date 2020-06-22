from db.database import *
from spotify import refresh_access_token


def is_access_token_expired(expiration_time):
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
    new_token = refresh_access_token(refresh_token)
    db.update_access_token_for_user(username, new_token)

