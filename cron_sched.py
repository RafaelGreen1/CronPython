import os
from apscheduler.schedulers.background import BlockingScheduler
def run_cron():
  os.system("python3 cron.py")

sched = BlockingScheduler()
sched.add_job(run_cron, 'interval', seconds =60) #will do the run_cron work for every 60 seconds

sched.start()