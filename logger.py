import sys
import time


class Logger:
    def __init__(self, file) -> None:
        self.origin = sys.stdout
        self.stdout = open(file=file, mode="a+")
        sys.stdout = self

    def write(self, message: str):
        lines = message.split('\n')

        for line in lines:
            if len(line) == 0:
                continue

            time_local = time.localtime()
            time_format = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            self.stdout.write("[{0}] {1}\n".format(time_format, line))
            self.stdout.flush()
