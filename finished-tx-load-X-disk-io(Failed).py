import csv

targets = __import__("targets")

transaction_indexes = targets.transaction_indexes
test_indexes = targets.test_indexes

transaction_idx = ""
test_idx = ""

hardware_log_header = None
elapsed_time_header = None


def read_data():
    global hardware_log_header
    global elapsed_time_header

    hardware_log_file = "./raw-data/" + transaction_idx + "-transactions/" + test_idx + "/hardware-log.csv"
    elapsed_time_file = "./results/elapsed-time-summaries/" + transaction_idx + "_" + test_idx + ".csv"

    with open(hardware_log_file, newline="") as csv_file:
        hardware_log = list(csv.reader(csv_file, delimiter=";"))
    with open(elapsed_time_file, newline="") as csv_file:
        elapsed_time = list(csv.reader(csv_file, delimiter=";"))

    hardware_log[0][0] = "timestamp(ms)"
    hardware_log_header = hardware_log[0]
    elapsed_time_header = elapsed_time[0]

    hardware_log.pop(0)
    elapsed_time.pop(0)

    # process_data(hardware_log, elapsed_time)

    joined_list = combine_data(hardware_log, elapsed_time)

    process_data(hardware_log, joined_list)


def combine_data(hardware_log, elapsed_time):
    for data in hardware_log:
        data.insert(1, None)

    joined_list = hardware_log + elapsed_time
    joined_list.sort(key=lambda x: x[0])

    return joined_list


def process_data(hardware_log, joined_list):
    load = 0
    prev_load = None
    i = 0

    for data in joined_list:
        if data[1] is None:
            print(['prev', 'load', prev_load, load])
            hardware_log[i].pop(1)
            if i != 0:
                hardware_log[i-1].append(prev_load)
                print(hardware_log[i-1])

            prev_load = load
            load = 0

            i += 1
            continue
        else:
            load += 1

    print(hardware_log_header)


def main():
    global test_idx
    global transaction_idx

    for transaction in transaction_indexes:
        for test in test_indexes:
            transaction_idx = transaction
            test_idx = test

            read_data()


if __name__ == "__main__":
    main()
