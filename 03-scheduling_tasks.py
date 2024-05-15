# Reference: https://docs.python.org/3/library/asyncio-task.html

import asyncio
import time


async def worker(delay, what):
    print(f"'{what}' started at {time.strftime('%X')}")
    await asyncio.sleep(delay)
    print(f"'{what}' done at {time.strftime('%X')}")


async def main():
    # asyncio.create_task()
    # Wrap the coro coroutine into a Task and schedule its execution. Return the Task object.
    # https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task

    task1 = asyncio.create_task(worker(1, "order milk"))
    task2 = asyncio.create_task(worker(2, "order bread"))

    print("done scheduling tasks.")

    await task1
    await task2


asyncio.run(main())

# TODO (1): what happens if task 1 takes 2 seconds, and task 2 takes 1 second?
