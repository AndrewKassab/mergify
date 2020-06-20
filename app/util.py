import time
from db.database import *


def is_access_token_expired(expiration_time):
    if time.time() > expiration_time:
        return True
    return False


def is_access_token_valid(access_token, username):
    pass
