# -*- coding: utf-8 -*-

import json

def class_to_dict(object):
    """
      Convert a jumpcloud object from an API request to a dictionary
    """
    result = []
    for item in object:
        result.append(item.__dict__)

    return result

def get_users_from_file(file):
    """
    Get users from a file
    :param file:
    :return:
    """
    try:
        with open(file, 'r') as f:
            users = json.load(f)

        return users
    except (ValueError, TypeError, FileNotFoundError, IOError) as e:
        raise e
