# Reference: https://docs.python.org/3/library/asyncio-task.html

import asyncio
import time


async def worker(delay, what):
    print(f"'{what}' started at {time.strftime('%X')}")
    await asyncio.sleep(delay)
    print(f"'{what}' done at {time.strftime('%X')}")


async def main():
    await worker(1, "order milk")
    await worker(2, "order bread")
    # NOTE: since coro "worker(2, "order bread")" is not scheduled yet, L15 exectues after the first coro is done

    # TODO: comment out L14-L15 and uncomment L20
    # how does asyncio.gather() make our coroutines run concurrently?
    # await asyncio.gather(worker(1, "order milk"), worker(2, "order bread"))


asyncio.run(main())
