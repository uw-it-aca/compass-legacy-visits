# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from commonconf.backends import use_configparser_backend
from uw_person_client import UWPersonClient


use_configparser_backend("/app/person.cfg", "compass")


uw_person = UWPersonClient()
known_netids = {}


def get_netid_from_student_number(student_number):
    try:
        return known_netids[student_number]
    except KeyError:
        person = uw_person.get_person_by_student_number(
            student_number, include_employee=False, include_student=True,
            include_student_transcripts=False,
            include_student_transfers=False, include_student_sports=False,
            include_student_advisers=False, include_student_majors=False,
            include_student_pending_majors=False,
            include_student_holds=False, include_student_degrees=False)
        if person.uwnetid is None:
            raise UnknownNetID(f"Unknown netid for {student_number}")

        known_netids[student_number] = person.uwnetid
        return person.uwnetid
