import csv

logs = []
test_numbers = ["1", "2", "3", "4", "5"]
tx_number = 100

log_summary = []


def read_log():
    global logs

    for i, number in enumerate(test_numbers):
        folder_path = (
            "./old-data/"
            + str(tx_number)
            + "-transactions/"
            + number
            + "/cpu-memory-log.csv"
        )
        with open(folder_path, newline="") as csvFile:
            logs.append(list(csv.reader(csvFile, delimiter=";")))


def processing_log():
    global logs
    global log_summary
    length = 0
    first_timestamps = []
    log_summary.append(
        [
            "timestamp-1(ms)",
            "cpu-used-1(%)",
            "ram-used-1(MB)",
            "disk-io-1(KB/s)",
            "timestamp-2(ms)",
            "cpu-used-2(%)",
            "ram-used-2(MB)",
            "disk-io-2(KB/s)",
            "timestamp-3(ms)",
            "cpu-used-3(%)",
            "ram-used-3(MB)",
            "disk-io-3(KB/s)",
            "timestamp-4(ms)",
            "cpu-used-4(%)",
            "ram-used-4(MB)",
            "disk-io-4(KB/s)",
            "timestamp-5(ms)",
            "cpu-used-5(%)",
            "ram-used-5(MB)",
            "disk-io-5(MB/s)",
        ]
    )

    for log in logs:
        del log[0]
        first_timestamps.append(int(log[0][0]))
        if len(log) > length:
            length = len(log)

    for idx in range(length):
        temp = []
        for j in range(5):
            if idx > len(logs[j]) - 1:
                temp.append(None)
                temp.append(None)
                temp.append(None)
                temp.append(None)
            else:
                temp.append(int(logs[j][idx][0]) - first_timestamps[j])
                temp.append(str(logs[j][idx][1]))
                temp.append(str(round(float(logs[j][idx][3]) / 1000000, 2)))
                temp.append(str(round(float(logs[j][idx][5]) / 1000000, 2)))

        log_summary.append(temp)


def write_csv():
    path = "./old-data/" + str(tx_number) + "-transactions/hardware-util-summary.csv"
    with open(path, mode="w", newline="") as csvFile:
        filewriter = csv.writer(csvFile, delimiter=";")
        filewriter.writerows(log_summary)


def main():
    read_log()
    processing_log()
    write_csv()


if __name__ == "__main__":
    main()
