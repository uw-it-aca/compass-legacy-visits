# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

#!/usr/bin/env python

from visits.dao.legacy import get_visits
from visits.dao.compass import store_visit
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
            store_visit(visit)
        except Exception as ex:
            logger.error(f"store_visit: {ex}")

    logger.info("conveyor: complete")


if __name__ == '__main__':
    convey(48)
