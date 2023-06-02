import argparse
import pathlib
import copy
import time
import asyncio
import numpy as np
from sys import float_info
from threading import Thread

def max_deviation(value, data):
    max_diff = float_info.min
    for other_value in data:
        diff = abs(value - other_value)
        if diff > max_diff:
            max_diff = diff

async def max_deviation_coroutine(value, data):
    return max_deviation(value, data)

async def run_coroutines(data):
    # Iterate over copied list
    data_cpy = copy.deepcopy(data)
    # Perform calculations using coroutines
    tasks = []
    for value in data_cpy:
        tasks.append(asyncio.create_task(max_deviation_coroutine(value, data)))
    await asyncio.gather(*tasks)

def threaded_main(data):
    # Iterate over copied list
    data_cpy = copy.deepcopy(data)

    # Perform calculations using Thread objects
    threads = list()
    # We include time to create and start the threads since this is notable overhead
    start_time = time.time_ns()
    for value in data_cpy:
        thd = Thread(target=max_deviation, args=[value, data])
        threads.append(thd)
        thd.start()

    for thd in threads:
        thd.join()
    stop_time = time.time_ns()
    thd_time = stop_time - start_time
    print(f"\narray_compare (threading):")
    print(f"\t{len(data)} calculations")
    print(f"\t{thd_time} ns")
    return thd_time

def async_main(data):
    start_time = time.time_ns()
    asyncio.run(run_coroutines(data))
    stop_time = time.time_ns()
    async_time = stop_time - start_time
    print(f"\narray_compare (asyncio):")
    print(f"\t{len(data)} calculations")
    print(f"\t{stop_time - start_time} ns")
    return async_time

def standard_main(data):
    # Iterate over copied list
    data_cpy = copy.deepcopy(data)
    # Perform calculations in a standard synchronous manner
    start_time = time.time_ns()
    for value in data_cpy:
        max_deviation(value, data)
    stop_time = time.time_ns()
    std_time = stop_time - start_time
    print(f"\narray_compare (standard):")
    print(f"\t{len(data)} calculations")
    print(f"\t{stop_time - start_time} ns")
    return std_time

def compare_time(std_time, other_time):
    direction = '-' if std_time > other_time else '+'
    time_delta = abs(std_time - other_time)
    print(f"\ttime difference: standard {direction} {time_delta} ns")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Find the maximum deviation of values")
    parser.add_argument('-n', '--sample_size', default=1000,  type=int)
    parser.add_argument('-i', '--input_path', default=None, type=pathlib.Path)
    args = parser.parse_args()

    data = np.array([])
    if args.input_path:
        # Data file must be sinle numbers on individual lines (i.e. "1\n2\n3\n")
        with args.input_path.open() as data_file:
            data_list = data_file.readlines().split('\n')
            if len(data_list) > args.sample_size:
                data = np.array(data_list[:args.sample_size])
            else:
                data = np.array(data_list)
    else:
        # create an array of random numbers in the range [0, 1)
        data = np.random.uniform(0, 1, args.sample_size)
    # Make data immutable
    data.flags["WRITEABLE"] = False

    # Perform calculations synchronously
    std_time = standard_main(data)
    # Perform calculations using threads
    thd_time = threaded_main(data)
    compare_time(std_time, thd_time)
    # Perform calculations using asyncio
    async_time = async_main(data)
    compare_time(std_time, async_time)
