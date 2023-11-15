#!/usr/bin/env python

# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from visits.dao.legacy import get_visits
from visits.dao.compass import store_visit
from datetime import datetime, timedelta
import pandas
import sys
import logging


def setup_logging():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    return logging.getLogger()


def convey():
    logger = setup_logging()
    logger.info("conveyor: start")

    d = datetime.today() - timedelta(days=1)

    logger.info(f"conveyor: gathering visits since {d}")

    try:
        visits = get_visits(d.strftime('%Y-%m-%d'))
    except Exception as ex:
        logger.error(f"get_visits: {ex}")

    for index, visit in visits.iterrows():
        try:
            store_visit(visit)
        except Exception as ex:
            logger.error(f"store_visit: {ex}")

    logger.info("conveyor: complete")


if __name__ == '__main__':
    convey()
