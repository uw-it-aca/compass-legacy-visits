# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import os
import pyodbc
import pandas


DB = os.getenv("LEGACY_DB_NAME")


def get_visits(since_date):
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
          Date >= '{since_date} 00:00:00.000'
          AND Contact_Type like 'IC%'
    """

    results = _run_query(DB, db_query)
    return results


def _run_query(database, query):
    os.environ["FREETDSCONF"] = "db_config/freetds.conf"
    os.environ["ODBCSYSINI"] = "db_config"

    user = os.getenv("LEGACY_DB_USERNAME")
    password = os.getenv("LEGACY_DB_PASSWORD")
    server = os.getenv("LEGACY_DB_HOST")
    constring = "Driver={FreeTDS};" \
                f"SERVERNAME={server};" \
                f"Database={database};" \
                "Port=1433;" \
                "TDS_Version=7.2;" \
                f"UID=netid.washington.edu\{user};" \
                f"PWD={password}"

    con = pyodbc.connect(constring)
    df = pandas.read_sql(query, con)
    del con
    return df
