# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

#from datetime import datetime, timedelta
#import pandas as pd
#import pyodbc
import os
import logging

logger = logging.getLogger(__name__)

mssql_driver = '{/opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.3.so.1.1}'
mssql_server = os.getenv('LEGACY_DB_HOST')
mssql_server_port = '1433'
mssql_database = os.getenv('LEGACY_DB_NAME')
mssql_username = os.getenv('LEGACY_DB_USERNAME')
mssql_password = os.getenv('LEGACY_DB_PASSWORD')

VISIT_API_HOST=os.getenv('VISITS_API_HOST')
VISIT_API_TOKEN=os.getenv('VISITS_API_TOKEN')

## open the connection
#cnxn = pyodbc.connect(
#    f"Driver={mssql_driver};"
#    f"Server={mssql_server},{mssql_server_port};"
#    f"Database={mssql_database};"
#    f"UID={mssql_username};"
#    f"PWD={mssql_password};")

#date = date.strftime("%Y-%m-%d")  # convert to format yyyy-mm-dd

# query for legacy i/c visits
#query = ("SELECT * FROM  WHERE checkin_date > '{date}'")

#data = pd.read_sql(query, cnxn)

# close the connection
#del cnxn

logging.info("Test message")
