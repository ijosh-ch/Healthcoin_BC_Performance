import time

script_1 = __import__("elapse-time-summary")
script_2 = __import__("elapse-time-X-monitor-log")
script_3 = __import__("tx-load-X-elapse-time")
script_4 = __import__("tx-load-X-monitor-log")
script_5 = __import__("mean-X-standard-deviation")


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
