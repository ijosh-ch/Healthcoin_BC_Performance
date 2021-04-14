import csv

targets = __import__("targets")

folders = targets.transaction_indexes
tests = targets.test_indexes

elapse_data = []
start_data = []
stop_data = []

tx_folder = ""
test_number = ""

folder_path = ""
elapse_path = ""


def read_data():
    global folder_path
    global start_data
    global stop_data

    elapse_data.clear()
    start_data.clear()
    stop_data.clear()

    folder_path = "./old-data/" + tx_folder + "-transactions/" + test_number + "/"
    start_path = folder_path + "start-summary.csv"
    stop_path = folder_path + "stop-summary.csv"

    # Read the star-summary.csv and stop-summary.csv
    with open(start_path, newline="") as csvFile:
        start_data = list(csv.reader(csvFile, delimiter=";"))
    with open(stop_path, newline="") as csvFile:
        stop_data = list(csv.reader(csvFile, delimiter=";"))


def process_data():
    global start_data
    global stop_data
    global elapse_data

    elapse_data.clear()
    # Create elapse-time summary
    for i, row in enumerate(start_data):
        if i == 0:
            elapse_data.append(row)
        else:
            elapse_data.append([])

            for j, col in enumerate(row):
                if j == 0:
                    elapse_data[i].append(col)
                else:
                    elapse_data[i].append(int(stop_data[i][j]) - int(col))


def write_data():
    global folder_path
    global elapse_data
    elapse_path = (
            folder_path + "elapse-time-summary-" + tx_folder + "_" + test_number + ".csv"
    )
    # Write the elapse-time summary into csv file
    with open(elapse_path, mode="w", newline="") as csvFile:
        file_writer = csv.writer(csvFile, delimiter=";")
        file_writer.writerows(elapse_data)


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
