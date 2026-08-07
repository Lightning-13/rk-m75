"""
RK M75 protocol constants.
"""

from __future__ import annotations

# --------------------------
# USB Device
# --------------------------

VENDOR_ID = 0x258A
PRODUCT_ID = 0x0163

USAGE_PAGE = 0xFF02
USAGE = 0x0001

INTERFACE = 1

# --------------------------
# HID Report
# --------------------------

REPORT_ID = 0x09
REPORT_SIZE = 520

HEADER = bytes.fromhex(
    "09 08 00 00 01 00 7A 01"
)

HEADER_SIZE = len(HEADER)

FRAME_SIZE = 378      # 126 RGB entries × 3 bytes
LED_COUNT = 126
RGB_SIZE = 3

PADDING_SIZE = REPORT_SIZE - HEADER_SIZE - FRAME_SIZE