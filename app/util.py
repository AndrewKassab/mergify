import time


def is_access_token_expired(access_token, expiration_time):
    if time.time() > expiration_time:
        return True
    return False