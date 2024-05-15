# Reference: https://docs.python.org/3/glossary.html#term-asynchronous-iterator

import asyncio
import time


async def dispatch_orders(delay):
    print(f"Started dispatching at {time.strftime('%X')}")
    for i in range(delay):
        await asyncio.sleep(1)
        yield i
    print(f"Done dispatching at {time.strftime('%X')}")


# TODO: uncomment this
# async def deliver_order(order):
#     await asyncio.sleep(1)
#     print(f"order {order} delivered {time.strftime('%X')}")


async def main():
    async with asyncio.TaskGroup() as tg:
        async for order in dispatch_orders(5):
            print(f"order {order} dispatched.")

            # TODO: uncomment this 
            # tg.create_task(deliver_order(order))


asyncio.run(main())
