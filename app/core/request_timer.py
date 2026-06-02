import time


class RequestTimer:

    def __init__(self):

        self.start_time = time.time()

    def elapsed(self):

        return round(
            time.time() - self.start_time,
            2
        )