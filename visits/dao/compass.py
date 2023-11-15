# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

#from uw_person_client import UWPersonClient
#from uw_person_client.exceptions import PersonNotFoundException
from datetime import datetime
import pytz


#uw_person = UWPersonClient()
known_netids = {}


def store_visit(visit):
    student_number = str(visit['student_no']).zfill(7)
    import pdb; pdb.set_trace()
    date = visit['Date']
    checkin = _get_checkin_date(visit)
    checkout = _get_checkout_date(visit)
    course_code = _get_course_code(visit)
    visit_type = visit['Contact_Type']

    print(f"{student_number}: {checkin} to {checkout}")


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


#def _get_student_netid(student_number):
#    try:
#        netid = known_netids[student_number]
#    except KeyError:
#        person = uw_person.get_person_by_student_number(
#            student_number, include_employee=False, include_student=True,
#            include_student_transcripts=False,
#            include_student_transfers=False, include_student_sports=False,
#            include_student_advisers=False, include_student_majors=False,
#            include_student_pending_majors=False,
#            include_student_holds=False, include_student_degrees=False)
#        netid = person.student.netid
#        known_netids[student_number] = netid
#        return netid
