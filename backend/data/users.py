"""
users.py
mock user records 
"""

from typing import List, Dict, Optional

# users are stored as a list of dictionaries
USERS: List[Dict[str, str]] = [
    {
        "id": "1",
        "first_name": "liam",
        "last_name": "cohen",
        "date_of_birth": "1989-03-14",  # age 36
        "job_title": "software engineer",
        "department": "Engineering",
        "email": "liam.cohen@company.com",
        "created_at": "2025-02-02T10:15:23Z",
    },
    {
        "id": "2",
        "first_name": "noa",
        "last_name": "levi",
        "date_of_birth": "1996-07-30",  # age 29
        "job_title": "hr generalist",
        "department": "HR",
        "email": "noa.levi@company.com",
        "created_at": "2025-03-14T08:03:11Z",
    },
    {
        "id": "3",
        "first_name": "david",
        "last_name": "rosen",
        "date_of_birth": "1982-01-09",  # age 43
        "job_title": "senior product manager",
        "department": "Marketing",
        "email": "david.rosen@company.com",
        "created_at": "2025-01-05T14:22:45Z",
    },
    {
        "id": "4",
        "first_name": "maya",
        "last_name": "katz",
        "date_of_birth": "1990-10-21",  # age 35
        "job_title": "data analyst",
        "department": "Finance",
        "email": "maya.katz@company.com",
        "created_at": "2024-11-18T09:12:07Z",
    },
    {
        "id": "5",
        "first_name": "amir",
        "last_name": "bar",
        "date_of_birth": "1985-05-02",  # age 40
        "job_title": "devops engineer",
        "department": "Engineering",
        "email": "amir.bar@company.com",
        "created_at": "2025-02-14T07:40:59Z",
    },
    {
        "id": "6",
        "first_name": "tal",
        "last_name": "shalev",
        "date_of_birth": "1970-12-19",  # age 54
        "job_title": "operations manager",
        "department": "Operations",
        "email": "tal.shalev@company.com",
        "created_at": "2024-10-01T16:33:21Z",
    },
    {
        "id": "7",
        "first_name": "yael",
        "last_name": "feldman",
        "date_of_birth": "1992-04-27",  # age 33
        "job_title": "marketing specialist",
        "department": "Marketing",
        "email": "yael.feldman@company.com",
        "created_at": "2025-03-03T11:05:13Z",
    },
    {
        "id": "8",
        "first_name": "ron",
        "last_name": "ben-ari",
        "date_of_birth": "1987-09-05",  # age 38
        "job_title": "account executive",
        "department": "Sales",
        "email": "ron.ben-ari@company.com",
        "created_at": "2024-09-22T13:49:00Z",
    },
    {
        "id": "9",
        "first_name": "eden",
        "last_name": "mizrahi",
        "date_of_birth": "1998-02-11",  # age 27
        "job_title": "finance associate",
        "department": "Finance",
        "email": "eden.mizrahi@company.com",
        "created_at": "2025-01-28T18:22:34Z",
    },
    {
        "id": "10",
        "first_name": "itay",
        "last_name": "oren",
        "date_of_birth": "1968-06-16",  # age 57
        "job_title": "solutions architect",
        "department": "Engineering",
        "email": "itay.oren@company.com",
        "created_at": "2024-08-10T07:58:12Z",
    },
    {
        "id": "11",
        "first_name": "shira",
        "last_name": "aviv",
        "date_of_birth": "1984-11-03",  # age 40
        "job_title": "people operations partner",
        "department": "HR",
        "email": "shira.aviv@company.com",
        "created_at": "2024-12-19T12:00:00Z",
    },
    {
        "id": "12",
        "first_name": "yair",
        "last_name": "shalom",
        "date_of_birth": "1993-08-25",  # age 32
        "job_title": "qa engineer",
        "department": "Engineering",
        "email": "yair.shalom@company.com",
        "created_at": "2025-02-01T09:30:44Z",
    },
    {
        "id": "13",
        "first_name": "ella",
        "last_name": "dahan",
        "date_of_birth": "1990-01-17",  # age 35
        "job_title": "content strategist",
        "department": "Marketing",
        "email": "ella.dahan@company.com",
        "created_at": "2024-11-25T21:14:07Z",
    },
    {
        "id": "14",
        "first_name": "dan",
        "last_name": "izraeli",
        "date_of_birth": "1975-03-08",  # age 50
        "job_title": "finance controller",
        "department": "Finance",
        "email": "dan.israeli@company.com",
        "created_at": "2024-07-29T06:12:55Z",
    },
    {
        "id": "15",
        "first_name": "lea",
        "last_name": "tal",
        "date_of_birth": "1980-05-26",  # age 45
        "job_title": "customer success manager",
        "department": "Sales",
        "email": "lea.tal@company.com",
        "created_at": "2024-10-12T15:45:39Z",
    },
    {
        "id": "16",
        "first_name": "asaf",
        "last_name": "zan",
        "date_of_birth": "1999-12-04",  # age 25
        "job_title": "junior software engineer",
        "department": "Engineering",
        "email": "asaf.zan@company.com",
        "created_at": "2025-03-22T10:10:10Z",
    },
    {
        "id": "17",
        "first_name": "tamar",
        "last_name": "golan",
        "date_of_birth": "1986-07-12",  # age 39
        "job_title": "brand manager",
        "department": "Marketing",
        "email": "tamar.golan@company.com",
        "created_at": "2024-12-30T08:08:08Z",
    },
    {
        "id": "18",
        "first_name": "nir",
        "last_name": "menachem",
        "date_of_birth": "1970-02-14",  # age 55
        "job_title": "head of operations",
        "department": "Operations",
        "email": "nir.menachem@company.com",
        "created_at": "2024-06-18T19:20:21Z",
    },
    {
        "id": "19",
        "first_name": "ruth",
        "last_name": "alon",
        "date_of_birth": "1979-09-29",  # age 46
        "job_title": "people n culture lead",
        "department": "HR",
        "email": "ruth.alon@company.com",
        "created_at": "2024-08-21T04:50:33Z",
    },
    {
        "id": "20",
        "first_name": "gal",
        "last_name": "peretz",
        "date_of_birth": "1996-06-01",  # age 29
        "job_title": "sales development representative",
        "department": "Sales",
        "email": "gal.peretz@company.com",
        "created_at": "2025-02-09T22:01:59Z",
    },
    {
        "id": "21",
        "first_name": "inbar",
        "last_name": "asher",
        "date_of_birth": "1988-04-05",  # age 37
        "job_title": "money analyst",
        "department": "Finance",
        "email": "inbar.asher@company.com",
        "created_at": "2025-01-11T12:34:56Z",
    },
]


def _strip_email(user: Dict[str, str]) -> Dict[str, str]:
    """
    create a copy of a user dict without the email
    i did this since nowdays emails is kinda regarded as a username, so we dont wanna expose user's data
    params:
        user (dict): the original user record including email
    returns:
        dict: a shallow copy of the user excluding email
    """
    # use dict comprehension to exclude the sensitive field
    return {k: v for k, v in user.items() if k != "email"}


def get_all_users() -> List[Dict[str, str]]:
    """
    return list of all users 

    returns:
        list[dict]: list of user dicts without email
    """
    return [_strip_email(u) for u in USERS]


# def get_user_by_id(user_id: int) -> Optional[Dict[str, str]]:
#     """
#     return single user by id , or None if not found.

#     params:
#         user_id (str): uuid of the requested user
#     returns:
#         dict | None: user dict without email, or None if there is no match
#     """
#     for u in USERS:
#         if u["id"] == user_id:
#             return _strip_email(u)
#     return None


def search_user_by_id(user_id: str) -> Optional[Dict[str, str]]:
    """
    search and return user by id (without email field), or None if not found.

    params:
        user_id (str): uuid to search for
    returns:
        dict | None: user dict without 'email' if found, otherwise None
    """
    # identical semantics to get_user_by_id; kept to satisfy the api contract
    for u in USERS:
        if u["id"] == user_id:
            return _strip_email(u)
    return None
