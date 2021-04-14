script_1 = __import__("original-data-extractor")
script_2 = __import__("elapsed-time-summary")
script_3 = __import__("elapsed-time-average")
script_4 = __import__("hardware-log-average")
script_5 = __import__("performance-average-summary")


def main():
    print("Run script 1...")
    script_1.main()
    print("Run script 2...")
    script_2.main()
    print("Run script 3...")
    script_3.main()
    print("Run script 4...")
    script_4.main()
    print("Run script 5...")
    script_5.main()


if __name__ == "__main__":
    main()
