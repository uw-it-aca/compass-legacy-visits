#!/bin/bash

# write person-client config

cat <<EOF > /app/person.cfg
[compass]
UW_PERSON_DB_USERNAME = $UW_PERSON_DB_USERNAME
UW_PERSON_DB_PASSWORD = $UW_PERSON_DB_PASSWORD
UW_PERSON_DB_HOSTNAME = $UW_PERSON_DB_HOSTNAME
UW_PERSON_DB_DATABASE = $UW_PERSON_DB_DATABASE
UW_PERSON_DB_PORT = $UW_PERSON_DB_PORT
EOF


# go into waiting around mode
tail -f /dev/null
