from __future__ import annotations

import time

from ..frame import Frame

from .device import RKM75Wireless
from .protocol import DYNAMIC_FPS, KEEPALIVE_FPS


class WirelessRGBStream:
    """
    Fixed-period wireless RGB stream.

    The current validated dynamic baseline is 14 FPS.

    The caller provides a frame_source(frame_index) function which
    returns an rkm75 Frame.
    """

    def __init__(
        self,
        device: RKM75Wireless,
        fps: float = DYNAMIC_FPS,
    ):
        if fps <= 0:
            raise ValueError(
                "fps must be positive."
            )

        if fps > DYNAMIC_FPS:
            raise ValueError(
                f"{DYNAMIC_FPS:g} FPS is the current validated "
                "dynamic baseline; higher rates are not yet "
                "supported by this wrapper."
            )

        self.device = device
        self.fps = float(fps)

    def run(
        self,
        frame_source,
        duration: float | None = None,
    ) -> int:
        """
        Run the wireless RGB stream.

        Args:
            frame_source:
                Callable receiving the current frame index and returning
                an rkm75 Frame.

            duration:
                Optional duration in seconds.

        Returns:
            Number of frames transmitted.
        """
        if duration is not None and duration <= 0:
            raise ValueError(
                "duration must be positive."
            )

        start = time.perf_counter()
        next_frame = start
        frame_index = 0

        while (
            duration is None
            or time.perf_counter() - start < duration
        ):
            frame = frame_source(frame_index)

            if not isinstance(frame, Frame):
                raise TypeError(
                    "frame_source must return an rkm75 Frame."
                )

            self.device.send_frame(frame)

            frame_index += 1
            next_frame += 1.0 / self.fps

            remaining = (
                next_frame - time.perf_counter()
            )

            if remaining > 0:
                time.sleep(remaining)
            else:
                # Do not accumulate unbounded scheduler debt.
                next_frame = time.perf_counter()

        return frame_index


class WirelessKeepalive:
    """
    Static RGB keepalive stream.

    The currently validated baseline is 5 FPS with the validated
    7 ms inter-report gap.

    The device must have transmitted at least one RGB frame before
    the keepalive can begin.
    """

    def __init__(
        self,
        device: RKM75Wireless,
        fps: float = KEEPALIVE_FPS,
    ):
        if fps <= 0:
            raise ValueError(
                "fps must be positive."
            )

        self.device = device
        self.fps = float(fps)

    def run(self, duration: float) -> int:
        """
        Repeat the last RGB transaction for duration seconds.

        Returns:
            Number of keepalive transactions transmitted.
        """
        if duration <= 0:
            raise ValueError(
                "duration must be positive."
            )

        start = time.perf_counter()
        next_tick = start
        sent = 0

        while (
            time.perf_counter() - start < duration
        ):
            self.device.send_keepalive()

            sent += 1
            next_tick += 1.0 / self.fps

            remaining = (
                next_tick - time.perf_counter()
            )

            if remaining > 0:
                time.sleep(remaining)
            else:
                # Do not accumulate scheduler debt.
                next_tick = time.perf_counter()

        return sent