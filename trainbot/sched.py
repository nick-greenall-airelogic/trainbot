import logging

from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(filename='./trainbot.log', level=logging.INFO)
_SCHED = BackgroundScheduler(prefix='trainbot-scheduler')


start = lambda : _SCHED.start()
stop = lambda : _SCHED.shutdown()


def set_user_reminder(user, destination, time, days, callback):
    def job_callback():
        logging.info('reminding {}'.format(user))
        callback(user, destination)
    active_reminder = _SCHED.get_job(user)
    if active_reminder:
        active_reminder.remove()
    time_parts = time.split(':')
    hour = time_parts[0]
    minute = time_parts[1]
    _SCHED.add_job(job_callback, trigger='cron', id=user, hour=hour, minute=minute, day_of_week=days)
