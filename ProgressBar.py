import time
import random


class ProgressBar:
    def __init__(self ,*args ,debug = False ,title = "Progress Bar"):
        if len(args) == 1:
            self.start, self.stop, = 0, args[0]
        elif len(args) == 2:
            self.start, self.stop = args[0], args[1]

        self.total = self.stop - self.start
        self.debug = debug
        self.time = time.time()
        self.progress = 1
        if not self.debug:
            text = title + ", " + str(self.total) + " steps"
            print("⌄" + text.center(38) + "⌄")


    def __iter__(self):
        current = self.start
        while current < self.stop:
            yield current
            current += 1

            if not self.debug:
                if current / self.total >= self.progress / 40.:
                    print("▮" ,end="")
                    self.progress += 1

        self.end()


    def end(self):
        if not self.debug:
            text = "Time taken: " + str(round(time.time() - self.time ,2)) + "s"
            print("\n⌃" + text.center(38) + "⌃\n")


if __name__ == '__main__':
    for i in ProgressBar(137 ,debug = False):
        time.sleep(random.random() / 8)

