import concurrent.futures
import time

start = time.perf_counter()


def do_something(seconds):
    print(f"Sleeping {seconds} second(s)...")
    time.sleep(seconds)
    return f"Done Sleeping...{seconds}"


# with concurrent.futures.ThreadPoolExecutor() as executor:
#     results = [executor.submit(do_something, 10) for _ in range(10)]
#     for f in concurrent.futures.as_completed(results):
#         print(f.result())


def main():

    with concurrent.futures.ProcessPoolExecutor() as executor:
        secs = [20, 20, 20, 20, 20, 20, 20, 20, 3, 3, 3]
        results = [executor.submit(do_something, i) for i in secs]
        for f in concurrent.futures.as_completed(results):
            print(f.result())

        # results = executor.map(do_something, secs)
        # for result in results:
        #     print(result)
    finish = time.perf_counter()

    print(f"Finished in {round(finish-start, 2)} second(s)")


if __name__ == "__main__":
    main()
