# -*- coding: utf-8 -*-
import requests

host = "https://vlinker2020.web.app"
data = [
    "ad34f389",
    "bd3f8c47",
    "0aa433d2",
    "a73cdae8"
]


def send_subject_to_drone(subjects, subject_id):
    address = host + "/api/services/" + data[subject_id]

    requests.get(address)
    print(subjects[subject_id])
