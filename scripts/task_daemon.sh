#!/bin/bash
set -e
set -o noglob

CMD="/scripts/task_daemon.py"

# quote for space within arguments
for i in "${@:1}"; do
    CMD="$CMD '$i'"
done

source "/app/bin/activate"

bash -c "$CMD"
