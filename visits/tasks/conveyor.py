#!/usr/bin/env python

# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

#from datetime import datetime, timedelta
#import pandas as pd
#import pyodbc
import os
import sys
import logging

mssql_driver = '{/opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.3.so.1.1}'
mssql_server = os.getenv('LEGACY_DB_HOST')
mssql_server_port = '1433'
mssql_database = os.getenv('LEGACY_DB_NAME')
mssql_username = os.getenv('LEGACY_DB_USERNAME')
mssql_password = os.getenv('LEGACY_DB_PASSWORD')

visit_api_host = os.getenv('VISITS_API_HOST')
visit_api_token = os.getenv('VISITS_API_TOKEN')

def setup_logging():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    return logging.getLogger()

def get_db_connection():
    return pyodbc.connect(
        f"Driver={mssql_driver};"
        f"Server={mssql_server},{mssql_server_port};"
        f"Database={mssql_database};"
        f"UID={mssql_username};"
        f"PWD={mssql_password};")

def close_db_connection(connection):
    del connection

def query(query, connection):
    return pd.read_sql(query, connection)

if __name__ == '__main__':
    logger = setup_logging()
    logger.info("conveyor start")

    # connection = get_db_connection()

    #date = date.strftime("%Y-%m-%d")  # convert to format yyyy-mm-dd

    # build sql for legacy i/c visits
    #sql = ("SELECT * FROM  WHERE checkin_date > '{date}'")

    #data = query(sql, connection)

    # close_db_connection(connection)

    logger.info("conveyor complete")
