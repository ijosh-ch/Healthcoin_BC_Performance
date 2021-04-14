import csv

targets = __import__("targets")

folders = targets.transaction_indexes
tests = targets.test_indexes

tx_folder = ""
test_number = ""


def read_data():
    global tx_folder
    global test_number

    folder_path = "./old-data/" + tx_folder + "-transactions/" + test_number + "/"
    stop_path = folder_path + "stop-summary.csv"

    elapse_path = (
            folder_path + "elapse-time-summary-" + tx_folder + "_" + test_number + ".csv"
    )

    cpu_memory_path = folder_path + "cpu-memory-log.csv"

    # Read the star-summary.csv and stop-summary.csv
    with open(stop_path, newline="") as csvFile:
        stop_data = list(csv.reader(csvFile, delimiter=";"))
    with open(elapse_path, newline="") as csvFile:
        elapse_data = list(csv.reader(csvFile, delimiter=";"))
    with open(cpu_memory_path, newline="") as csvFile:
        cpu_log = list(csv.reader(csvFile, delimiter=";"))

    del stop_data[0]
    del elapse_data[0]
    del cpu_log[0]

    process_data(stop_data, elapse_data, cpu_log)


def process_data(stop_data, elapse_data, cpu_log):
    stop_elapse_cpu_data = []

    for i, row in enumerate(stop_data):
        for j, data in enumerate(row):
            if j == 0:
                continue

            stop_elapse_cpu_data.append([int(data), elapse_data[i][j]])

    for i, data in enumerate(cpu_log):
        temp = [
            int(data[0]),
            None,
            round(float(data[1]), 2),
            round(float(data[2]), 2),
            round(float(data[3]) / 1000000, 2),
            data[4],
            round(float(data[5]) / 1000000, 2),
        ]
        stop_elapse_cpu_data.append(temp)

    stop_elapse_cpu_data.sort(key=lambda x: x[0])

    # Simplified the timestamp
    initial_time = stop_elapse_cpu_data[0][0]
    for i, data in enumerate(stop_elapse_cpu_data):
        data[0] = data[0] - initial_time

    stop_elapse_cpu_data.insert(
        0,
        [
            "timestamp(ms)",
            "elapse-time(ms)",
            "cpu-usage-pid(%)",
            "cpu-usage-total(%)",
            "memory-used-pid(MB)",
            "memory-usage-total(%)",
            "disk-io-total(MB/s)",
        ],
    )

    write_data(stop_elapse_cpu_data)


def write_data(start_elapse_cpu_data):
    global tx_folder
    global test_number
    # Write the elapse-time summary into csv file
    start_elapse_cpu_path = (
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

    with open(start_elapse_cpu_path, mode="w", newline="") as csvFile:
        file_writer = csv.writer(csvFile, delimiter=";")
        file_writer.writerows(start_elapse_cpu_data)


def main():
    global tx_folder
    global test_number

    for i, folder in enumerate(folders):
        for test in tests[i]:
            tx_folder = folder
            test_number = test

            read_data()


if __name__ == "__main__":
    main()
