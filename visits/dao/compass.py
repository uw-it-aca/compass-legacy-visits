# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from commonconf.backends import use_configparser_backend
from uw_person_client import UWPersonClient
from datetime import datetime
import urllib3
import pytz
import os


use_configparser_backend("/app/person.cfg", "compass")


uw_person = UWPersonClient()
known_netids = {}


def store_visit(visit):
    student_no = str(visit['student_no']).zfill(7)
    visit_data = {
        "student_netid": _get_netid(student_no),
        "visit_type": _get_visit_type(visit),
        "course_code": _get_course_code(visit),
        "checkin_date": _get_checkin_date(visit),
        "checkout_date": _get_checkout_date(visit)
    }

    _store_visit_data(visit_data)


def _store_visit_data(visit_data):
    host = os.getenv('VISITS_API_HOST')
    token = os.getenv('VISITS_API_TOKEN')
    url = f"http://{host}/api/v1/visit/omad"

    http = urllib3.PoolManager()
    headers = urllib3.make_headers(authorization=f"Bearer {token}")
    response = http.urlopen('POST', url, headers=headers, data=visit_data)


def _get_visit_type(visit):
    return visit['Contact_Type']


def _get_course_code(visit):
    return visit['Event_Type'] or "None"


def _get_checkin_date(visit):
    pacific = pytz.timezone('US/Pacific')
    naive_date = datetime.strptime(visit['Date'], '%Y-%m-%d %H:%M:%S.%f')
    date = pacific.localize(naive_date)
    time = datetime.strptime(visit['Time_In'], '%H:%M:%S')
    return date.replace(
        hour=time.hour,
        minute=time.minute,
        second=time.second).astimezone(pytz.utc)


def _get_checkout_date(visit):
    pacific = timezone('US/Pacific')
    naive_date = datetime.strptime(visit['Date'], '%Y-%m-%d %H:%M:%S.%f')
    date = pacific.localize(naive_date)
    time = datetime.strptime(visit['Time_Out'], '%H:%M:%S')
    return date.replace(
        hour=time.hour,
        minute=time.minute,
        second=time.second).astimezone(pytz.utc)


def _get_netid(student_number):
    try:
        netid = known_netids[student_number]
    except KeyError:
        person = uw_person.get_person_by_student_number(
            student_number, include_employee=False, include_student=True,
            include_student_transcripts=False,
            include_student_transfers=False, include_student_sports=False,
            include_student_advisers=False, include_student_majors=False,
            include_student_pending_majors=False,
            include_student_holds=False, include_student_degrees=False)
        known_netids[student_number] = person.student.uwnetid
        return person.student.uwnetid
