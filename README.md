# SQLAlchemy Workshop

## No More Raw SQL: SQLAlchemy, ORMs and asyncio

This repository contains the code for the Marketplace service demo to follow along the **No More Raw SQL: SQLAlchemy, ORMs and asyncio workshop**.

**Workshop instructions can be found [here](https://aelsayed95.github.io/sqlalchemy-wkshop/)**

### How to run this service?

1. Create a python virtual environment and activate it:

    ```sh
    python3.12 -m venv ./venv
    source ./venv/bin/activate
    ```

2. Install your service dependencies:

    ```sh
    python3.12 -m pip install -r requirements.txt
    ```

3. Run the service:

    ```sh
    ./run.sh run
    ```

    which is equivalent to

    ```sh
    python3.12 marketsvc/server.py
    ```

4. In a new terminal window, run the `curl` commands:

    ```sh
    ./run.sh customers
    ```

    which is equivalent to

    ```sh
    curl http://localhost:9090/api/customers
    ```
