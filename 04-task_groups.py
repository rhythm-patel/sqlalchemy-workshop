# Reference: https://docs.python.org/3/library/asyncio-task.html

import asyncio
import time


async def worker(delay, what):
    print(f"{what} started at {time.strftime('%X')}")
    await asyncio.sleep(delay)
    print(f"{what} done at {time.strftime('%X')}")


async def main():
    # asyncio.TaskGroup() - new in Python3.11
    # https://docs.python.org/3/library/asyncio-task.html#asyncio.TaskGroup
    async with asyncio.TaskGroup() as tg:
        tg.create_task(worker(1, "order milk"))
        tg.create_task(worker(2, "order bread"))
        print("scheduling done")

    # The await is implicit when the context manager exits.
    print("Done.")

asyncio.run(main())
