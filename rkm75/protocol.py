"""
Protocol constants discovered during reverse engineering.
"""

from __future__ import annotations

REPORT_ID = 0x09

FEATURE_REPORT_SIZE = 520

HEADER_SIZE = 8

HEADER = bytes.fromhex(
    "09 08 00 00 01 00 7A 01"
)

VENDOR_ID = 0x258A

PRODUCT_ID = 0x0163

USAGE_PAGE = 0xFF02

USAGE = 0x0001

INTERFACE = 1