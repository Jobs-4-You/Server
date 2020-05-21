import asyncio
import logging.config
import time

from j4u_api.config import config
from j4u_api.qualtrics.get_features import get_features
from j4u_api.utils.func import async_timeit

logging.config.fileConfig("logging.ini")
logger = logging.getLogger(__name__)


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
        f = async_timeit(__name__)(get_features)
        asyncio.create_task(interval_job(f, [], int(config.GET_FEATURES_JOB_INTERVAL)))
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
