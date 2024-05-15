# Example inspired by https://realpython.com/async-io-python/#the-event-loop-and-asynciorun
import asyncio
import random
import time
from dataclasses import dataclass, field

ITEMS = [
    "milk",
    "eggs",
    "crepes",
    "rice",
    "bread",
    "tomatoes",
    "cucumbers",
    "fish",
    "chicken",
    "shrimp",
]
MAX_ITEMS = 5
MAX_SLEEP = 5
MAX_TASKS = 3


@dataclass
class Order:
    created: float = field(init=False)
    item: str

    def __post_init__(self):
        self.created = time.perf_counter()

    def __repr__(self):
        return self.item


async def place_order(cid: int, q: asyncio.Queue):
    num_items = random.randint(1, MAX_ITEMS)
    print(f"Customer={cid} is online")
    for i in range(num_items):
        await asyncio.sleep(random.randint(1, MAX_SLEEP))  # browsing time

        item_id = random.randint(0, len(ITEMS) - 1)
        order = Order(ITEMS[item_id])
        print(f"Customer id={cid} placed an order={order}")

        await q.put(order)
        print(f"Customer id={cid}'s order={order} sent successfully")


async def process_orders(shop_id: int, q: asyncio.Queue):
    print(f"Shop id={shop_id} ready to receive orders")
    try:
        while True:
            order = await q.get()

            print(f"Shop id={shop_id} processing order={order}")
            await asyncio.sleep(random.randint(1, MAX_SLEEP))

            now = time.perf_counter()
            print(
                f"Shop id={shop_id} processed order={order} in {now - order.created:0.3f}"
            )
            q.task_done()
    except asyncio.exceptions.CancelledError:
        print(f"Shop id={shop_id} is now closed.")


async def main():
    # asyncio.Queue()
    # https://docs.python.org/3/library/asyncio-queue.html
    q = asyncio.Queue()

    customers = [
        asyncio.create_task(place_order(n, q)) for n in range(MAX_TASKS)
    ]
    shops = [
        asyncio.create_task(process_orders(n, q)) for n in range(MAX_TASKS)
    ]

    await asyncio.gather(*customers)
    await q.join()  # awaits shops too

    for shop in shops:
        shop.cancel()
    print("Done.")


asyncio.run(main())
