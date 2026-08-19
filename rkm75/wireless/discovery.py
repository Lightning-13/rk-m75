from __future__ import annotations

import hid

from .protocol import (
    PID,
    USAGE,
    USAGE_PAGE,
    VID,
)


def discover():
    """
    Find the RK M75 2.4 GHz RGB HID interface.
    """

    for dev in hid.enumerate(VID, PID):
        path = dev["path"]

        if (
            dev["usage_page"] == USAGE_PAGE
            and dev["usage"] == USAGE
            and b"MI_01" in path
            and b"Col01" in path
        ):
            return dev

    raise RuntimeError(
        "RK M75 2.4 GHz RGB HID interface not found."
    )