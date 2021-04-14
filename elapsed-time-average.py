import csv
import statistics

targets = __import__("targets")

transaction_indexes = targets.transaction_indexes
test_indexes = targets.test_indexes

transaction_idx = ""
test_idx = ""

elapsed_time = []
averages = []


def read_data():
    file_path = "./results/elapsed-time-summaries/" + transaction_idx + "_" + test_idx + ".csv"

    with open(file_path, newline="") as csv_file:
        temp = list(csv.reader(csv_file, delimiter=";"))

    # Remove the header
    temp.pop(0)

    # Concat the elapsed_time list
    for data in temp:
        elapsed_time.append(int(data[1]))


def process_data():
    averages.append(
        [
            transaction_idx,
            round(statistics.mean(elapsed_time), 2)
        ]
    )


def write_data():
    file_name = "./results/elapsed-time-summaries/elapsed-time-averages.csv"

    with open(file_name, mode="w", newline="") as csv_file:
        file_writer = csv.writer(csv_file, delimiter=";")
        file_writer.writerows(averages)


def main():
    global test_idx
    global transaction_idx

    for transaction in transaction_indexes:
        elapsed_time.clear()

        # Concat the elapsed_time for every transaction index
        for test in test_indexes:
            test_idx = test
            transaction_idx = transaction

            read_data()

        # Calculate every transaction elapsed-time average value
        process_data()

    # Add header to the list
    averages.insert(0, ["tx-amount/peer", "elapsed-time(ms)"])
    write_data()


if __name__ == "__main__":
    main()
