"""
This is an example RPC client that connects to the RPyC based scheduler service.
It first connects to the RPyC server on localhost:12345.
Then it schedules a job to run on 2 second intervals and sleeps for 10 seconds.
After that, it unschedules the job and exits.
"""

from time import sleep

import rpyc

conn = rpyc.connect("localhost", 12345)
job = conn.root.add_job(
    "run_scheduler:get_features_and_send_emails",
    trigger="interval",
    id="test",
    replace_existing="true",
    seconds=15,
)
conn.root.print_jobs()
sleep(10)
conn.root.remove_job("test")
