import time


DEFAULT_FPS = 33.0
MAX_FPS = 33.0


class RGBStream:
    def __init__(self, device, fps=DEFAULT_FPS):
        if fps <= 0:
            raise ValueError("FPS must be greater than 0.")

        if fps > MAX_FPS:
            raise ValueError(
                f"FPS must not exceed {MAX_FPS:g} for the current "
                "RK M75 streaming implementation."
            )

        self.device = device
        self.fps = fps
        self.interval = 1.0 / fps
        self._next_send = None

    def __enter__(self):
        self._next_send = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._next_send = None

    def send(self, frame):
        if self._next_send is None:
            raise RuntimeError("RGBStream must be used as a context manager.")

        now = time.perf_counter()

        if now < self._next_send:
            time.sleep(self._next_send - now)

        self.device.send(frame)

        self._next_send += self.interval

        # If the caller took longer than one interval, don't try to
        # "catch up" with a burst of reports.
        if self._next_send < time.perf_counter():
            self._next_send = time.perf_counter()