"""
RK M75 2.4 GHz wireless RGB backend.

This module exposes the currently validated wireless RGB path.

The wireless protocol is only partially reverse-engineered. The public
implementation currently supports the recovered six-group RGB path and
its validated packet transport.
"""

from .device import RKM75Wireless
from .protocol import (
    DYNAMIC_FPS,
    KEEPALIVE_FPS,
    INTER_REPORT_GAP_MS,
    NATIVE_PAYLOAD_SIZE,
    REPORT_SIZE,
    packetize,
    reconstruct,
    report_count_for_stream,
    validate_transaction,
)
from .stream import (
    WirelessKeepalive,
    WirelessRGBStream,
)
from .encoder import (
    NativeGroup,
    SIX_GROUP_LAYOUT,
    TWELVE_GROUP_LAYOUT,
    encode_native_groups,
    frame_to_six_groups,
    encode_frame_six_groups,
    frame_to_twelve_groups,
    encode_frame_twelve_groups,
)

__all__ = [
    "DYNAMIC_FPS",
    "KEEPALIVE_FPS",
    "INTER_REPORT_GAP_MS",
    "NATIVE_PAYLOAD_SIZE",
    "REPORT_SIZE",
    "RKM75Wireless",
    "WirelessKeepalive",
    "WirelessRGBStream",
    "packetize",
    "reconstruct",
    "report_count_for_stream",
    "validate_transaction",
    "NativeGroup",
    "SIX_GROUP_LAYOUT",
    "TWELVE_GROUP_LAYOUT",
    "encode_native_groups",
    "frame_to_six_groups",
    "encode_frame_six_groups",
    "frame_to_twelve_groups",
    "encode_frame_twelve_groups",
]