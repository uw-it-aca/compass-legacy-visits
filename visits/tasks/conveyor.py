# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

#!/usr/bin/env python

from visits.dao.legacy import get_visits
from visits.dao.compass import store_visit
from visits.exceptions import (
    MissingCheckInTime, MissingCheckOutTime, UnknownNetID)
from datetime import datetime, timedelta
import pandas
import sys
import logging


def setup_logging():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    return logging.getLogger()


def convey(hours=48):

    logger = setup_logging()
    logger.info("conveyor: start")

    since_date = datetime.today() - timedelta(hours=hours)

    logger.info(f"conveyor: gathering visits since {since_date}")

    try:
        visits = get_visits(since_date)
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
    convey(48)
