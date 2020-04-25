import time

import rpyc
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from rpyc.utils.server import ThreadedServer

from j4u_api.app.app import app
from j4u_api.config import config
from j4u_api.qualtrics.get_features import get_features
from j4u_api.utils.mail import send_mails

jobstores = {"default": SQLAlchemyJobStore(url=config.DB_URL)}
executors = {"default": ProcessPoolExecutor(4)}
job_defaults = {"coalesce": False, "max_instances": 3}

scheduler = BackgroundScheduler(
    jobstores=jobstores, executors=executors, job_defaults=job_defaults
)


def get_features_and_send_emails():
    users = get_features()
    with app.app_context():
        if users is not None and len(users) > 0:
            tos = [[user.email] for user in users]
            print(tos)
            kwargs_list = [{"link": f"{config.APP_URL}/?login"}] * len(users)
            send_mails(
                tos=tos,
                subject="Données importées avec succès",
                template="export-done",
                kwargs_list=kwargs_list,
            )


class SchedulerService(rpyc.Service):
    def exposed_add_job(self, func, *args, **kwargs):
        return scheduler.add_job(func, *args, **kwargs)

    def exposed_modify_job(self, job_id, jobstore=None, **changes):
        return scheduler.modify_job(job_id, jobstore, **changes)

    def exposed_reschedule_job(
        self, job_id, jobstore=None, trigger=None, **trigger_args
    ):
        return scheduler.reschedule_job(job_id, jobstore, trigger, **trigger_args)

    def exposed_print_jobs(self):
        return scheduler.print_jobs()

    def exposed_pause_job(self, job_id, jobstore=None):
        return scheduler.pause_job(job_id, jobstore)

    def exposed_resume_job(self, job_id, jobstore=None):
        return scheduler.resume_job(job_id, jobstore)

    def exposed_remove_job(self, job_id, jobstore=None):
        scheduler.remove_job(job_id, jobstore)

    def exposed_get_job(self, job_id):
        return scheduler.get_job(job_id)

    def exposed_get_jobs(self, jobstore=None):
        return scheduler.get_jobs(jobstore)


if __name__ == "__main__":
    scheduler = BackgroundScheduler(
        jobstores=jobstores, executors=executors, job_defaults=job_defaults
    )
    scheduler.start()
    protocol_config = {"allow_public_attrs": True}
    server = ThreadedServer(
        SchedulerService, port=12345, protocol_config=protocol_config
    )
    try:
        server.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        scheduler.shutdown()
