#!/usr/bin/env python

# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from visits.dao.legacy import get_visits
from visits.dao.compass import store_visit
from visits.exceptions import (
    MissingCheckInTime, MissingCheckOutTime, UnknownNetID)
from datetime import datetime, timedelta
import argparse
import pandas
import sys
import logging


def setup_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.addFilter(lambda record: record.levelno <= logging.INFO)
    logger.addHandler(handler)

    handler = logging.StreamHandler()
    handler.setLevel(logging.WARNING)
    logger.addHandler(handler)

    return logger


def convey(hours=48):
    logger = setup_logging()

    since_date = datetime.today() - timedelta(hours=hours)

    logger.info(f"conveyor: gather previous {hours} hours ({since_date})")

    try:
        visits = get_visits(since_date)
        logger.info(f"store_visit: processing {len(visits)} legacy visits")
    except Exception as ex:
        logger.error(f"get_visits: {ex}")

    for index, visit in visits.iterrows():
        try:
            visit_data = store_visit(visit)
            logger.info(f"store_visit: added {visit_data['student_netid']} "
                        f"for {visit_data['course_code']}: "
                        f"{visit_data['checkin_date']} to "
                        f"{visit_data['checkout_date']}")
        except MissingCheckInTime as ex:
            logger.info(f"store_visit: {ex}")
        except (Exception, MissingCheckOutTime, UnknownNetID) as ex:
            logger.error(f"store_visit: {ex}")

    logger.info("conveyor: complete")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convey legacy DB I/C Visits into Compass')
    parser.add_argument(
        'hours', type=int,
        help='previous hours of events to convey')
    args = parser.parse_args()

    convey(args.hours)
