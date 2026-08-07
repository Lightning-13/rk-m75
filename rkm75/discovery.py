from __future__ import annotations

import hid

from .protocol import PRODUCT_ID
from .protocol import USAGE
from .protocol import USAGE_PAGE
from .protocol import VENDOR_ID


def discover():

    for dev in hid.enumerate(VENDOR_ID, PRODUCT_ID):

        if (
            dev["usage_page"] == USAGE_PAGE
            and dev["usage"] == USAGE
            and b"MI_01" in dev["path"]
            and b"Col05" in dev["path"]
        ):
            return dev

    raise RuntimeError(
        "RK M75 RGB HID interface not found."
    )