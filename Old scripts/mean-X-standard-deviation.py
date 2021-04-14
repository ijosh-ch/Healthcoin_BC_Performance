import csv
import numpy as np
import matplotlib.pyplot as plt
import os

targets = __import__("targets")

folders = targets.transaction_indexes
tests = targets.test_indexes

tx_folder = ""
test_number = ""

elapse_time = None
monitor_log = None

mean_log = None
std_log = None
mean_elapse = None
std_elapse = None

monitor_log_result = None
elapse_time_result = None


def read_data():
    global elapse_time
    global monitor_log

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

    with open(file_path, newline="") as csvFile:
        monitor_log = list(csv.reader(csvFile, delimiter=";"))

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

    with open(file_path, newline="") as csvFile:
        elapse_time = list(csv.reader(csvFile, delimiter=";"))

    del monitor_log[0]
    del elapse_time[0]


def process_data():
    global monitor_log
    global elapse_time
    global mean_log
    global std_log
    global mean_elapse
    global std_elapse
    global monitor_log_result
    global elapse_time_result

    mean_log = [
        ["Transaction Load"],
        ["CPU Usage Average"],
        ["Memory Usage Average"],
        ["Disk I/O Usage Average"],
    ]
    std_log = [["CPU Usage(%)"], ["RAM Usage(MB)"], ["Disk I/O Usage(MB/s)"]]
    mean_elapse = [["Transaction Load"], ["Average Elapse Time"]]
    std_elapse = [["Elapse Time(ms)"]]

    for data in monitor_log:
        data[1] = int(data[1])
        data[2] = float(data[2])
        data[4] = float(data[4])
        data[6] = float(data[6])

    for data in elapse_time:
        data[1] = int(data[1])
        data[2] = int(data[2])

    monitor_log.sort(key=lambda x: x[1])
    elapse_time.sort(key=lambda x: x[2])

    all_log_data = [
        ["Tx-Load"],
        ["CPU-Usage(%)"],
        ["RAM-Usage(MB)"],
        ["Disk-I/O-Usage(MB/s)"],
    ]

    log_temp = [
        [],
        [],
        [],
    ]
    for i, data in enumerate(monitor_log):
        if data[1] == 0:
            continue

        all_log_data[0].append(data[1])  # tx-load
        all_log_data[1].append(data[2])  # cpu
        all_log_data[2].append(data[4])  # ram
        all_log_data[3].append(data[6])  # disk

        if data[1] == monitor_log[i - 1][1]:
            log_temp[0].append(data[2])  # cpu
            log_temp[1].append(data[4])  # ram
            log_temp[2].append(data[6])  # disk
        else:
            if log_temp[0]:
                for j in range(len(mean_log)):
                    if j == 0:
                        mean_log[j].append(monitor_log[i - 1][1])  # tx-load
                    else:
                        mean_log[j].append(round(np.mean(log_temp[j - 1]), 2))
                        std_log[j - 1].append(round(np.std(log_temp[j - 1]), 2))

            log_temp = [
                [data[2]],
                [data[4]],
                [data[6]],
            ]

        if i == len(monitor_log) - 1:
            for j in range(len(mean_log)):
                if j == 0:
                    mean_log[j].append(monitor_log[i][1])
                else:
                    mean_log[j].append(round(np.mean(log_temp[j - 1]), 2))
                    std_log[j - 1].append(round(np.std(log_temp[j - 1]), 2))

    all_elapse_data = [["Tx-Load"], ["Elapse-Time(ms)"]]
    elapse_temp = []
    for i, data in enumerate(elapse_time):
        all_elapse_data[0].append(data[2])
        all_elapse_data[1].append(data[1])

        if data[2] == elapse_time[i - 1][2] or i == 0:
            elapse_temp.append(data[1])
        else:
            if elapse_temp:
                mean_elapse[0].append(elapse_time[i - 1][2])
                mean_elapse[1].append(round(np.mean(elapse_temp), 2))
                std_elapse[0].append(round(np.std(elapse_temp), 2))

            elapse_temp = [data[1]]

        if i == len(elapse_time) - 1:
            if elapse_temp:
                mean_elapse[0].append(elapse_time[i][2])
                mean_elapse[1].append(round(np.mean(elapse_temp), 2))
                std_elapse[0].append(round(np.std(elapse_temp), 2))

    # Count Regression
    regression = [[], [], [], []]
    for i in range(4):
        if i < 3:
            regression[i] = reg_linear(mean_log[0], mean_log[i + 1])
        else:
            regression[i] = reg_linear(mean_elapse[0], mean_elapse[1])

    # Plot the graph
    names = ["cpu", "ram", "disk", "elapse-time"]
    for i, name in enumerate(names):
        fig_path = (
                "./old-data/graphics/"
                + name
                + "/"
                + name
                + "-"
                + tx_folder
                + "_"
                + test_number
                + ".png"
        )

        if i < 3:
            plot_graph(
                mean_log[0],  # x_mean = tx-load
                mean_log[i + 1],  # y_mean = cpu / ram / disk
                std_log[i],
                all_log_data[0],
                all_log_data[i + 1],
                regression[i][0],
                regression[i][1],
                fig_path,
            )
        else:
            plot_graph(
                mean_elapse[0],
                mean_elapse[1],
                std_elapse[0],
                all_elapse_data[0],
                all_elapse_data[1],
                regression[i][0],
                regression[i][1],
                fig_path,
            )

    monitor_log_result = []
    for i in range(len(mean_log[0])):
        monitor_log_result.append(
            [
                mean_log[0][i],
                mean_log[1][i],
                mean_log[2][i],
                mean_log[3][i],
                std_log[0][i],
                std_log[1][i],
                std_log[2][i],
            ]
        )

    elapse_time_result = []
    for i in range(len(std_elapse[0])):
        elapse_time_result.append(
            [mean_elapse[0][i], mean_elapse[1][i], std_elapse[0][i]]
        )


def plot_graph(x_mean, y_mean, err_mean, x_raw, y_raw, x_reg, y_reg, file_path):
    transaction_text = 'Transaction' if tx_folder == '1' else "Transactions"

    title = (
            "Comparison Between the Number of "
            + x_mean[0]
            + "\nwith the "
            + y_mean[0] + " Value"
            + "\nin Experiment Number-"
            + str(test_number)
            + ",\n(Scenario: "
            + tx_folder + ' '
            + transaction_text
            + " per Peer)"
    )

    plt.figure(figsize=(12, 8))
    plt.title(title)
    plt.xlabel(x_raw[0])
    plt.ylabel(y_raw[0])

    x = x_raw[1:]
    y = y_raw[1:]

    # Plot Raw old-data
    plt.scatter(x, y, label="Value of " + err_mean[0], s=100, color="darkgrey", marker="x")

    x = x_mean[1:]
    y = y_mean[1:]
    e = err_mean[1:]

    # Plot Mean
    plt.errorbar(
        x,
        y,
        e,
        marker="o",
        linestyle="None",
        capsize=3,
        label="Mean & Deviation Value of\n" + err_mean[0],
        color="blue",
        ecolor="red",
    )

    # Plot Trend Line
    plt.plot(x_reg, y_reg, color="green", label="Trend Line of " + err_mean[0])

    plt.grid()
    plt.legend()
    plt.savefig(file_path)
    # plt.show()
    plt.close()


def reg_linear(x_input, y_input):
    x = np.array(x_input[1:])
    y = np.array(y_input[1:])

    # number of observations/points
    n = np.size(x)

    # mean of x and y vector
    m_x, m_y = np.mean(x), np.mean(y)

    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y * x) - n * m_y * m_x
    SS_xx = np.sum(x * x) - n * m_x * m_x

    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1 * m_x

    y_pred = b_0 + b_1 * x

    return x, y_pred


def write_data():
    global tx_folder
    global test_number
    global monitor_log_result
    global elapse_time_result

    # Write the elapse-time summary into csv file
    monitor_log_path = (
            "./old-data/"
            + tx_folder
            + "-transactions/"
            + test_number
            + "/mean-std-tx-load-X-monitor-log-"
            + tx_folder
            + "_"
            + test_number
            + ".csv"
    )

    elapse_time_path = (
            "./old-data/"
            + tx_folder
            + "-transactions/"
            + test_number
            + "/mean-std-tx-load-X-elapse-time-"
            + tx_folder
            + "_"
            + test_number
            + ".csv"
    )

    with open(monitor_log_path, mode="w", newline="") as csvFile:
        filewriter = csv.writer(csvFile, delimiter=";")
        filewriter.writerows(monitor_log_result)

    with open(elapse_time_path, mode="w", newline="") as csvFile:
        filewriter = csv.writer(csvFile, delimiter=";")
        filewriter.writerows(elapse_time_result)


def check_path():
    names = ["cpu", "ram", "disk", "elapse-time"]

    if not os.path.exists("../old-data/graphics/"):
        os.mkdir("../old-data/graphics/")

    for name in names:
        path = "./old-data/graphics/" + name + "/"
        if not os.path.exists(path):
            os.mkdir(path)


def main():
    global tx_folder
    global test_number

    check_path()

    for i, folder in enumerate(folders):
        for test in tests[i]:
            print(str(folder) + "_" + str(test))
            tx_folder = folder
            test_number = test

            read_data()
            process_data()
            # write_data()


if __name__ == "__main__":
    main()
