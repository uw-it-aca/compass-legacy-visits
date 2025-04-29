#!/usr/bin/env python

# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from visits.dao.legacy import get_visits
from visits.dao.compass import store_visit
from visits.exceptions import (
    MissingCheckInTime, MissingCheckOutTime, UnknownNetID)
from datetime import datetime, timedelta
import argparse
import pandas
import sys
import os
import logging


def setup_logging(name):
    # send all logging to stderr.  task_daemon.py invokes this
    # via subprocess check_output which siphons off stdout
    logging.basicConfig(level=logging.DEBUG)
    return logging.getLogger(name)


def convey(hours=48):
    logger = setup_logging("convey")

    since_date = datetime.today() - timedelta(hours=hours)

    logger.info(f"gather previous {hours} hours ({since_date})")

    try:
        visits = get_visits(since_date)
        logger.info(f"processing {len(visits)} legacy visits")
    except Exception as ex:
        logger.error(f"get_visits: {ex}")

    for index, visit in visits.iterrows():
        try:
            visit_data = store_visit(visit)
            logger.info(f"add {visit_data['student_netid']} "
                        f"for {visit_data['course_code']}: "
                        f"{visit_data['checkin_date']} to "
                        f"{visit_data['checkout_date']}")
        except MissingCheckInTime as ex:
            logger.info(f"store_visit: {ex}")
        except (Exception, MissingCheckOutTime, UnknownNetID) as ex:
            logger.error(f"store_visit: {ex}")

    logger.info("complete")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convey legacy DB I/C Visits into Compass')
    parser.add_argument(
        'hours', type=int,
        help='previous hours of events to convey')
    args = parser.parse_args()

    convey(args.hours)
