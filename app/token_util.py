import time
from db.database import db
from spotify import refresh_access_token


def is_users_access_token_expired(user_id):
    expiration_time = db.get_expiration_time_for_user(user_id)
    if time.time() > expiration_time:
        return True
    return False


def is_auth_token_valid(auth_token):
    return db.does_auth_token_exist(auth_token)


def refresh_and_update_access_token_for_user(user_id):
    refresh_token = db.get_refresh_token_for_user(user_id)
    new_token = refresh_access_token(refresh_token)['access_token']
    db.update_access_token_for_user(user_id, new_token)
    return new_token

