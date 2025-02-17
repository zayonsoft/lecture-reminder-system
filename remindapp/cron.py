from django_cron import CronJobBase, Schedule
from remindapp.tasks import sendReminderMail

class DailyReminderCronjob(CronJobBase):
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'remindapp.daily_reminder'
    
    def do(self):
        print("Code is Working....")
        sendReminderMail()