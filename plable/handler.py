from typing import Counter
from kosapy import Kosapy

from requests.sessions import session
from datetime import datetime
from plable.components import parse_slot
from plable.components import Parallel

faculty = "fit"
user = "94e86e19-51f9-4cfa-9c1a-872e482538d1"
password = "rzdYZ5VI5xhfb9rblHyvQynSAw8Ogk1s"

import numpy as np
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from requests.auth import  HTTPBasicAuth
from plable.renderer import render

def get_session(user, password, auth_endpoint="auth.fit.cvut.cz"):
    auth = HTTPBasicAuth(user, password)
    client = BackendApplicationClient(client_id=user)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=f"https://{auth_endpoint}/oauth/oauth/token", auth=auth)
    return oauth


kosapy = Kosapy(f"https://kosapi.{faculty}.cvut.cz/api/3b/", None, session=get_session(user, password))
# kosapy.use_cache(True)


def get_parallels(classes: list[str], semester: str) -> list[Parallel]:
    # classes = ["BI-ZMA", "BI-MLO", "BI-CAO", "BI-PA1", "BI-PS1", "BI-PAI"]
    parallels = {}
    counters = {}
    #  course, course_fullname, semester, type, parallel_no, occupied, capacity, teachers:set, slots:list
    for code in classes:
        collected = {}
        counters[code] = {}
        for x in kosapy.courses.get(code).parallels(sem=semester):
            if x.occupied() < x.capacity():
                if x.parallelType() not in collected:
                    collected[x.parallelType()] = []
                    counters[code][x.parallelType()] = 0

                p = Parallel(
                    code,
                    x.course(),
                    semester,
                    x.parallelType(),
                    x.code(),
                    x.occupied(),
                    x.capacity(),
                    {y.__call__() for y in x.teacher} if isinstance(x.teacher, list) or isinstance(x.teacher, tuple) else {x.teacher()},
                    [parse_slot(y) for y in x.timetableSlot]
                    if isinstance(x.timetableSlot, list)
                    else [parse_slot(x.timetableSlot)],
                )

                collected[x.parallelType()].append(p)
                counters[code][x.parallelType()] += 1
        parallels[code] = collected

    return parallels, counters

