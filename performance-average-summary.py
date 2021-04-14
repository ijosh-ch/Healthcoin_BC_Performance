import csv

averages = []
headers = []


def read_data():
    file_paths = [
        './results/elapsed-time-summaries/elapsed-time-averages.csv',
        './results/hardware-log-summaries/hardware-log-pid-averages.csv',
        './results/hardware-log-summaries/hardware-log-total-averages.csv'
    ]

    for path in file_paths:
        with open(path, newline="") as csv_file:
            temp = list(csv.reader(csv_file, delimiter=";"))
        averages.append(temp)


def process_data():
    for average in averages:
        headers.append(average[0])
        average.pop(0)

    # Insert elapsed-time average into every hardware-log
    for i in range(4):
        averages[1][i].insert(1, averages[0][i][1])
        averages[2][i].insert(1, averages[0][i][1])

    # Create the header for each files
    headers[1].insert(1, headers[0][1])
    headers[2].insert(1, headers[0][1])

    # Remove the elapsed-time average & header
    averages.pop(0)
    headers.pop(0)

    for i, header in enumerate(headers):
        averages[i].insert(0, header)


def write_data():
    file_names = [
        './results/performance-averages-pid.csv',
        './results/performance-averages-total.csv'
    ]

    for i, file_name in enumerate(file_names):
        with open(file_name, mode="w", newline="") as csv_file:
            file_writer = csv.writer(csv_file, delimiter=";")
            file_writer.writerows(averages[i])


def main():
    read_data()
    process_data()
    write_data()


if __name__ == "__main__":
    main()
