import csv

targets = __import__("targets")

folders = targets.transaction_indexes
tests = targets.test_indexes

timestamp = []
monitor_data = []
tx_folder = "100"
test_number = "1"


def read_data():
    global monitor_data
    global timestamp

    monitor_data.clear()
    timestamp.clear()

    file_path = (
            "./old-data/"
            + tx_folder
            + "-transactions/"
            + test_number
            + "/elapse-time-X-monitor-log-"
            + tx_folder
            + "_"
            + test_number
            + ".csv"
    )

    log = []

    with open(file_path, newline="") as csvFile:
        log = list(csv.reader(csvFile, delimiter=";"))

    del log[0]

    start_time = int(log[0][0])

    for data in log:
        data[0] = int(data[0]) - start_time

        if len(data) > 2:
            monitor_data.append(data)
        else:
            timestamp.append([data[0], data[0] + int(data[1])])


def process_data():
    global monitor_data
    global timestamp
    del_idx = []

    for data in monitor_data:
        time_limit = data[0]
        tx_load = 0
        del_idx.clear()

        for tx_time in timestamp:
            if tx_time[0] > time_limit:
                break
            else:
                tx_load += 1
                if tx_time[1] < time_limit:
                    del_idx.append(tx_time)

        for item in del_idx:
            timestamp.remove(item)

        data[1] = tx_load

    monitor_data.insert(
        0,
        [
            "timestamp(ms)",
            "tx-load",
            "cpu-usage-pid(%)",
            "cpu-usage-total(%)",
            "memory-used-pid(MB)",
            "memory-usage-total(%)",
            "disk-io-total(MB/s)",
        ],
    )


def write_data():
    global monitor_data

    file_path = (
            "./old-data/"
            + tx_folder
            + "-transactions/"
            + test_number
            + "/tx-load-X-monitor-log-"
            + tx_folder
            + "_"
            + test_number
            + ".csv"
    )

    with open(file_path, mode="w", newline="") as csvFile:
        filewriter = csv.writer(csvFile, delimiter=";")
        filewriter.writerows(monitor_data)


def main():
    global tx_folder
    global test_number

    for i, folder in enumerate(folders):
        for i, test in enumerate(tests[i]):
            tx_folder = folder
            test_number = test

            read_data()
            process_data()
            write_data()


if __name__ == "__main__":
    main()
