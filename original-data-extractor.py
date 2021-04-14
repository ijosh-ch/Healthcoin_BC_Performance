import os
import shutil


def copytree(src, dst, symlink=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)

        if os.path.isdir(s):
            shutil.copytree(s, d, symlink, ignore)
        else:
            shutil.copy2(s, d)


def main():
    targets = __import__("targets")

    folders = targets.transaction_indexes
    targets = targets.test_indexes

    for folder in folders:
        for target in targets:
            path = str(folder) + "-transactions/" + str(target) + "/"

            source = "./old-data/" + path
            destination = "./raw-data/" + path

            files = ['cpu-memory-log.csv', 'start-summary.csv', 'stop-summary.csv']

            for file in files:
                os.makedirs(os.path.dirname(destination), exist_ok=True)
                if file == 'cpu-memory-log.csv':
                    shutil.copyfile(source + file, destination + 'hardware-log.csv')
                else:
                    shutil.copyfile(source + file, destination + file)


if __name__ == "__main__":
    main()
