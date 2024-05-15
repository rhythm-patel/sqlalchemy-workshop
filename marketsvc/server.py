import asyncio

import uvicorn
from db.init_db import init_db
from db_accessor import (
    add_new_order_for_customer,
    get_customers,
    get_orders_between_dates,
    get_orders_of_customer,
    get_total_cost_of_an_order,
)
from fastapi import FastAPI, HTTPException, Request, status

app = FastAPI(debug=True)


@app.get("/")
def hello():
    return "Welcome to Marketplace!"


@app.get("/api/customers")
async def customers():
    return [customer.as_dict() async for customer in get_customers()]


@app.get("/api/orders/{cust_id}")
async def orders(cust_id: int):
    orders = await get_orders_of_customer(cust_id)
    response = [order.as_dict() for order in orders]
    return response


@app.get("/api/order_total/{order_id}")
async def order_total(order_id: int):
    total = await get_total_cost_of_an_order(order_id)
    return {"Order Total": total}


@app.get("/api/orders_total")
async def orders_total(request: Request):
    json = await request.json()
    orders = json.get("orders", [])
    async with asyncio.TaskGroup() as tg:
        order_tasks = [
            tg.create_task(get_total_cost_of_an_order(order))
            for order in orders
        ]
    return [task.result() for task in order_tasks]


@app.get("/api/orders_between_dates/{before}/{after}")
async def orders_between_dates(before: str, after: str):
    orders_gen = get_orders_between_dates(after, before)
    return [order.as_dict() async for order in orders_gen]


@app.post("/api/add_new_order", status_code=status.HTTP_201_CREATED)
async def add_new_order(request: Request):
    json = await request.json()
    customer_id = json.get("customer_id")
    items = json.get("items")

    success = await add_new_order_for_customer(customer_id, items)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


async def main():
    config = uvicorn.Config(
        "server:app", host="127.0.0.1", port=9090, reload=True
    )
    server = uvicorn.Server(config)
    await init_db()
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
