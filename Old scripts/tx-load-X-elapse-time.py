import csv

targets = __import__("targets")

folders = targets.transaction_indexes
tests = targets.test_indexes

timestamp = []
tx_folder = ""
test_number = ""


def read_data():
    global timestamp

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

        if len(data) == 2:
            timestamp.append([data[0], data[0] + int(data[1])])


def process_data():
    global timestamp

    for i, time_now in enumerate(timestamp):
        load = 1

        if i > 0:
            for j in range(i):
                if timestamp[i - 1 - j][1] > time_now[0]:
                    load += 1
                else:
                    break

        for j in range(len(timestamp) - i - 1):
            if timestamp[i + 1 + j][0] < time_now[1]:
                load += 1
            else:
                break

        time_now.append(load)

    for data in timestamp:
        data[1] = data[1] - data[0]

    timestamp.insert(
        0, ["timestamp(ms)", "elapse-time(ms)", "tx-load",],
    )


def write_data():
    global timestamp

    file_path = (
        "./old-data/"
        + tx_folder
        + "-transactions/"
        + test_number
        + "/elapse-time-X-tx-load-"
        + tx_folder
        + "_"
        + test_number
        + ".csv"
    )

    with open(file_path, mode="w", newline="") as csvFile:
        filewriter = csv.writer(csvFile, delimiter=";")
        filewriter.writerows(timestamp)


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
