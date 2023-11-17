# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from visits.dao.person import get_netid_from_student_number
from visits.exceptions import (
    MissingCheckInTime, MissingCheckOutTime, UnknownNetID)
from datetime import datetime
import requests
import json
import pytz
import os


def store_visit(visit):
    student_no = str(visit['student_no']).zfill(7)
    netid = get_netid_from_student_number(student_no)
    visit_data = {
        'student_netid': netid,
        'visit_type': _get_visit_type(visit),
        'course_code': _get_course_code(visit),
    }

    try:
        visit_data['checkin_date'] = _get_date(visit, 'Time_In')
    except AttributeError:
        raise MissingCheckInTime(
            f"{netid} for {visit_data['course_code']} has no checkin time")

    try:
        visit_data['checkout_date'] = _get_date(visit, 'Time_Out')
    except AttributeError:
        raise MissingCheckOutTime(
            f"{netid} for {visit_data['course_code']} at "
            f"visit_data['checkin_date'] has no exit time")

    _store_visit_data(visit_data)
    return visit_data


def _get_visit_type(visit):
    return visit['Contact_Type']


def _get_course_code(visit):
    return visit['Event_Type'] or "None"


def _get_date(visit, in_or_out):
    pacific = pytz.timezone('US/Pacific')
    naive_date = datetime.strptime(visit['Date'].split(' ')[0], '%Y-%m-%d')
    date = pacific.localize(naive_date)
    time = datetime.strptime(visit[in_or_out].split('.')[0], '%H:%M:%S')

    return date.replace(
        hour=time.hour,
        minute=time.minute,
        second=time.second).astimezone(pytz.utc).isoformat()


def _store_visit_data(visit_data):
    host = os.getenv('VISITS_API_HOST')
    token = os.getenv('VISITS_API_TOKEN')
    headers = {'Authorization': f"Token {token}"}
    url = f"http://{host}/api/v1/visit/omad"

    response = requests.post(
        url, headers=headers, json=json.dumps(visit_data))

    if response.status_code not in [200, 201]:
        raise Exception(
            f"{response.status_code}: for {visit_data['student_netid']}")
