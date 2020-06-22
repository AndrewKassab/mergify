from db.database import *


def is_access_token_expired(expiration_time):
    if time.time() > expiration_time:
        return True
    return False


def is_access_token_valid(access_token, username):
    actual_token = db.get_access_token_for_user(username)
    if access_token == actual_token:
        return True
    return False
