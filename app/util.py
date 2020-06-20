import time


def is_access_token_expired(expiration_time):
    timenow = time.time
    if time.time() > expiration_time:
        return True
    return False