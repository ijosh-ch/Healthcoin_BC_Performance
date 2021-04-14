import csv
import statistics
import os

targets = __import__("targets")

transaction_indexes = targets.transaction_indexes
test_indexes = targets.test_indexes

transaction_idx = ""
test_idx = ""

hardware_log = []
averages_total = []
averages_pid = []


def read_data():
    file_path = "./raw-data/" + transaction_idx + "-transactions/" + test_idx + "/hardware-log.csv"

    with open(file_path, newline="") as csv_file:
        temp = list(csv.reader(csv_file, delimiter=";"))

    temp.pop(0)

    for data in temp:
        hardware_log.append(data)


def process_data():
    cpu_pid_log = []
    cpu_total_log = []
    ram_pid_log = []
    ram_total_log = []
    disk_total_log = []

    for data in hardware_log:
        cpu_pid_log.append(float(data[1]))
        cpu_total_log.append(float(data[2]))
        ram_pid_log.append(int(data[3]))
        ram_total_log.append(float(data[4]))
        disk_total_log.append(float(data[5]))

    averages_total.append([
        transaction_idx,
        str(round(statistics.mean(cpu_pid_log), 2)),
        str(round(statistics.mean(ram_pid_log) / 1000000, 2)),
        str(round(statistics.mean(disk_total_log) / 1000000, 2)),
        str(round(statistics.mean(cpu_total_log), 2)),
        str(round(statistics.mean(ram_total_log), 2))
    ])


def write_data():
    folder_name = './results/hardware-log-summaries/'
    file_names = ['hardware-log-pid-averages.csv',
                  'hardware-log-total-averages.csv']

    averages = [averages_pid, averages_total]

    os.makedirs(os.path.dirname(folder_name), exist_ok=True)

    for i, file_name in enumerate(file_names):
        with open(folder_name + file_name, mode="w", newline="") as csv_file:
            file_writer = csv.writer(csv_file, delimiter=";")
            file_writer.writerows(averages[i])


def main():
    global test_idx
    global transaction_idx
    global hardware_log_header

    for transaction in transaction_indexes:
        hardware_log.clear()

        # Concat the elapsed_time for every transaction index
        for test in test_indexes:
            test_idx = test
            transaction_idx = transaction

            read_data()

        # Calculate every transaction elapsed-time average value
        process_data()

    hardware_log_header = [
        'tx-amount/peer',
        'cpu-usage-pid(%)',
        'memory-usage-pid(MB)',
        'disk-io-usage-total(MB/s)',
        'cpu-usage-total(%)',
        'memory-usage-total(%)'
    ]

    # Add header to the list
    averages_total.insert(0, hardware_log_header)

    for data in averages_total:
        averages_pid.append(
            [data[0], data[1], data[2], data[3]]
        )

    write_data()


if __name__ == "__main__":
    main()
