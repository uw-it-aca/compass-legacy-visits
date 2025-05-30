#!/usr/bin/env python

# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from call_command import CallCommand
import sys


TASK_DIRECTORY="/app/visits/tasks"


#
# Run task on a continuous loop
# periodically based on a "--delay <seconds>" or
# "--cron '* * * * *'" specification, and gracefully
# exit on termination signal
#
def main():
    default_loop_delay = 15
    loop_delay = None
    cron_spec = None
    command = None
    options = []
    our_arg = True

    # sift daemon from task arguments
    for arg in sys.argv[1:]:
        if our_arg:
            if loop_delay is not None and len(loop_delay) == 0:
                loop_delay = arg
            elif cron_spec is not None and len(cron_spec) == 0:
                cron_spec = arg
            elif arg == '--delay':
                loop_delay = ""
            elif arg == '--cron':
                cron_spec = ""
            elif arg == '--':
                our_arg = False
            else:
                command = arg
                our_arg = False
        elif not command:
            command = arg
            our_arg = False
        else:
            options.append(arg)

    if loop_delay is None and cron_spec is None:
        loop_delay = default_loop_delay
    CallCommand(is_daemon=True,
                command=f'{TASK_DIRECTORY}/{command}.py',
                options=options,
                cron_spec=cron_spec,
                loop_delay=loop_delay).run()


if __name__ == '__main__':
    main()
