__author__ = "dale mcdiarmid"

import re
import os.path


def modify_list(values=[], pattern="", replacement="", ignorecase=False):
    """ Perform a `re.sub` on every item in the list"""
    if ignorecase:
        flags = re.I
    else:
        flags = 0
    _re = re.compile(pattern, flags=flags)
    return [_re.sub(replacement, value) for value in values]


def append_to_list(values=[], suffix=""):
    if isinstance(values, str):
        values = values.split(",")
    return [str(value + suffix) for value in values]


def array_to_str(values=[], separator=","):
    return separator.join(values)


def extract_role_users(users={}, exclude_users=[]):
    role_users = []
    for user, details in list(users.items()):
        if user not in exclude_users and "roles" in details:
            for role in details["roles"]:
                role_users.append(role + ":" + user)
    return role_users


def filename(filename=""):
    return os.path.splitext(os.path.basename(filename))[0]


def _is_reserved(details):
    """Return True when an Elasticsearch user/role entry is flagged as reserved."""
    return (
        "metadata" in details
        and "_reserved" in details["metadata"]
        and bool(details["metadata"]["_reserved"])
    )


def remove_reserved(user_roles={}):
    """Return the names of the entries that are NOT reserved."""
    return [name for name, details in user_roles.items() if not _is_reserved(details)]


def filter_reserved(users_role={}):
    """Return the names of the entries that ARE reserved."""
    return [name for name, details in users_role.items() if _is_reserved(details)]


class FilterModule(object):
    def filters(self):
        return {
            "modify_list": modify_list,
            "append_to_list": append_to_list,
            "filter_reserved": filter_reserved,
            "array_to_str": array_to_str,
            "extract_role_users": extract_role_users,
            "remove_reserved": remove_reserved,
            "filename": filename,
        }
