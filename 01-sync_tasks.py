import time


def worker(delay, what):
    print(f"'{what}' started at {time.strftime('%X')}")
    time.sleep(delay)
    print(f"'{what}' done at {time.strftime('%X')}")


def main():
    jobs = ["order milk", "order bread", "order eggs"]
    for job in jobs:
        worker(1, job)


if __name__ == "__main__":
    main()
