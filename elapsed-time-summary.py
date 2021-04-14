import csv
import os

targets = __import__("targets")

transaction_indexes = targets.transaction_indexes
test_indexes = targets.test_indexes

start_timestamps = []
stop_timestamps = []
elapsed_times = []

transaction_idx = ""
test_idx = ""


def read_data():
    global start_timestamps
    global stop_timestamps

    start_timestamps.clear()
    stop_timestamps.clear()
    elapsed_times.clear()

    folder_path = "./raw-data/" + transaction_idx + "-transactions/" + test_idx + "/"

    with open(folder_path + "start-summary.csv", newline="") as csv_file:
        start_timestamps = list(csv.reader(csv_file, delimiter=";"))

    with open(folder_path + "stop-summary.csv", newline="") as csv_file:
        stop_timestamps = list(csv.reader(csv_file, delimiter=";"))

    process_data()


def process_data():
    global start_timestamps
    global stop_timestamps
    global elapsed_times

    # Left only the timestamp values on the lists
    remove_headers(start_timestamps)
    remove_headers(stop_timestamps)

    # Record the stop timestamps with the elapsed time of every transactions
    for i, layer_1 in enumerate(stop_timestamps):
        for j, stop in enumerate(layer_1):
            elapsed_times.append([stop, int(stop) - int(start_timestamps[i][j])])

    # Sort the list
    elapsed_times.sort(key=lambda x: x[0])

    # Add header for elapsed_times list
    elapsed_times.insert(0, ["stop-timestamps(ms)", "elapsed-time(ms)"])

    write_csv(elapsed_times)


def write_csv(data):
    destination = "./results/elapsed-time-summaries/"
    file_name = destination + transaction_idx + "_" + test_idx + ".csv"

    # Create folder
    os.makedirs(os.path.dirname(destination), exist_ok=True)

    with open(file_name, mode="w", newline="") as csv_file:
        file_writer = csv.writer(csv_file, delimiter=";")
        file_writer.writerows(data)


def remove_headers(array):
    array.pop(0)
    for layer_1 in array:
        layer_1.pop(0)


def main():
    global test_idx
    global transaction_idx

    for transaction in transaction_indexes:
        for test in test_indexes:
            test_idx = test
            transaction_idx = transaction

            read_data()


if __name__ == "__main__":
    main()
