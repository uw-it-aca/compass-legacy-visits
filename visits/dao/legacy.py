# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import pyodbc
import pandas
from datetime import datetime, timedelta
import warnings
import os


DB = os.getenv("LEGACY_DB_NAME")


def get_visits(since_date):
    date = since_date.strftime('%Y-%m-%d')
    time = since_date.strftime('%H:%M:%S')

    time_clause = f"( Date >= '{date} 00:00:00.000' AND Time_In >= '{time}' )"
    now = datetime.now()
    if since_date.date() < now.date():
        next_day = (since_date + timedelta(days=1)).strftime('%Y-%m-%d')
        time_clause = f"( {time_clause} OR Date >= '{next_day} 00:00:00.000' )"

    db_query = f"""
        SELECT
            student_no,
            Contact_Type,
            Date,
            Time_In,
            Time_Out,
            Event_Type
        FROM
            appointment
        WHERE
            {time_clause}
            AND Contact_Type like 'IC%'
    """
    results = _run_query(DB, db_query)
    return results


def _run_query(database, query):
    os.environ["FREETDSCONF"] = "db_config/freetds.conf"
    os.environ["ODBCSYSINI"] = "db_config"

    user = os.getenv("LEGACY_DB_USERNAME")
    password = os.getenv("LEGACY_DB_PASSWORD")
    constring = "Driver={FreeTDS};" \
                "SERVERNAME=compass;" \
                f"Database={database};" \
                "Port=1433;" \
                "TDS_Version=7.2;" \
                f"UID=netid.washington.edu\{user};" \
                f"PWD={password}"

    con = pyodbc.connect(constring)

    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')
        df = pandas.read_sql(query, con)

    del con
    return df
