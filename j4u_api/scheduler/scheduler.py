import asyncio
import logging.config
import time
from datetime import datetime

from j4u_api.app.app import app
from j4u_api.config import config
from j4u_api.database.connection import db_session
from j4u_api.database.models import DatetimeJob as DatetimeJobModel
from j4u_api.database.models import User as UserModel
from j4u_api.qualtrics import qual_client
from j4u_api.qualtrics.get_features import get_features
from j4u_api.utils.func import async_timeit
from j4u_api.utils.mail import send_mails

logging.config.fileConfig("logging.ini")
logger = logging.getLogger(__name__)


async def get_features_and_send_emails():
    users = await get_features()
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
    return len(users)


async def exec_campaigns():
    # Get campaigns to execute
    campaigns = DatetimeJobModel.query.filter(
        DatetimeJobModel.state == "PENDING",
        DatetimeJobModel.execution_date < datetime.now(),
    ).all()
    print(f"{len(campaigns)} mail campaigns to execute")

    # Execute campaings
    for campaign in campaigns:
        campaign.state = "PROCESSING"
        db_session.commit()

        params = campaign.params
        users = UserModel.query.filter(
            UserModel.form_done_at >= params["cohortStart"],
            UserModel.form_done_at <= params["cohortEnd"],
            UserModel.group_id.in_(params["groupId"]),
        ).all()
        valid_emails = [u.email for u in users] + [
            "test@yopmail.com",
            "yap@yopmail.com",
            "jimi.vaubien@protonmail.com",
            "doriana.tinello@gmail.com",
            "Tinah.Raniriharinosy@etu.unige.ch",
            "Marion.Mueller@etu.unige.ch",
            "ioana.medeleine.c@gmail.com",
            "clemence.gallopin@unil.ch",
            "guillaume.rais.1@unil.ch",
            "carole.marullaz@gmail.com",
        ]
        links = qual_client.get_distribution_links(
            params["distribId"], params["surveyId"]
        )
        for l in links:
            print(l["email"])
        print(valid_emails)
        emails, links = zip(
            *[(l["email"], l["link"]) for l in links if l["email"] in valid_emails]
        )
        print(emails)
        print(valid_emails)

        with app.app_context():
            if len(emails) > 0:
                tos = [[email] for email in emails]
                print(tos)
                kwargs_list = [
                    {"link": link, "expiration": str(params["surveyEnd"])}
                    for link in links
                ]
                send_mails(
                    tos=tos,
                    subject="Entrainement",
                    template="training-survey",
                    kwargs_list=kwargs_list,
                )

        campaign = DatetimeJobModel.query.get(campaign.id)
        campaign.state = "SUCCESS"
        print(list(emails))
        pp = dict(campaign.params)
        pp["emailsMatched"] = list(emails)
        print(pp)
        campaign.params = pp
        db_session.add(campaign)
        db_session.commit()


async def coro(start, i):
    laps = int(time.time() - start)
    print(f"Elapsed: {laps} -- {i}")


async def interval_job(coro, args, interval):
    while True:
        try:
            await coro(*args)
        except Exception as err:
            print(err)
        await asyncio.sleep(interval)


class Job:
    def __init__(self, coro, args):
        pass


class IntervalJob(Job):
    def __init__(self, coro, args):
        pass


class DatetimeJob(Job):
    def __init__(self, coro, args):
        pass


def abc():
    logger.info("ajiol")


class Scheduler:
    def __init__(self):
        pass

    def start(self):
        asyncio.run(self.main())

    async def main(self):
        f = async_timeit(__name__)(get_features_and_send_emails)
        asyncio.create_task(interval_job(f, [], int(config.GET_FEATURES_JOB_INTERVAL)))
        asyncio.create_task(interval_job(exec_campaigns, [], 15))
        while True:
            await asyncio.sleep(10)

        pass


# async def main():
#    print("Start scheduler loop")
#
#    start = time.time()
#
#    asyncio.create_task(interval_job(get_features, [], 15))
#
#    while True:
#        await asyncio.sleep(5)


# asyncio.get_event_loop().run_until_complete(main())
# asyncio.run().run_until_complete(main())
