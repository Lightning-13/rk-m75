from __future__ import annotations

import ctypes
import time
from ctypes import wintypes

from .protocol import REPORT_SIZE


kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
hid_dll = ctypes.WinDLL("hid", use_last_error=True)


CreateFileW = kernel32.CreateFileW
CreateFileW.argtypes = [
    wintypes.LPCWSTR,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.LPVOID,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.HANDLE,
]
CreateFileW.restype = wintypes.HANDLE


CloseHandle = kernel32.CloseHandle
CloseHandle.argtypes = [wintypes.HANDLE]
CloseHandle.restype = wintypes.BOOL


HidD_SetOutputReport = hid_dll.HidD_SetOutputReport
HidD_SetOutputReport.argtypes = [
    wintypes.HANDLE,
    wintypes.LPVOID,
    wintypes.ULONG,
]
HidD_SetOutputReport.restype = wintypes.BOOLEAN


GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002
OPEN_EXISTING = 3

INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value


class WirelessHidTransport:
    """
    Windows HID transport for the RK M75 2.4 GHz RGB interface.

    This deliberately uses the same Windows HID output-report mechanism
    as the previously validated 2.4 GHz implementation.
    """

    def __init__(
        self,
        path: bytes | str,
        gap_ms: float = 7.0,
    ):
        if gap_ms < 0:
            raise ValueError(
                "gap_ms must not be negative."
            )

        if isinstance(path, bytes):
            path = path.decode("utf-8")

        self.path = path
        self.gap_ms = float(gap_ms)

        self._handle = None
        self._closed = True

    def open(self):
        if not self._closed:
            return

        handle = CreateFileW(
            self.path,
            GENERIC_READ | GENERIC_WRITE,
            FILE_SHARE_READ | FILE_SHARE_WRITE,
            None,
            OPEN_EXISTING,
            0,
            None,
        )

        if handle == INVALID_HANDLE_VALUE:
            raise ctypes.WinError(
                ctypes.get_last_error()
            )

        self._handle = handle
        self._closed = False

    def _ensure_open(self):
        if self._closed or self._handle is None:
            raise RuntimeError(
                "Wireless HID transport is closed."
            )

    def send_report(self, report: bytes) -> float:
        """
        Send one 20-byte HID output report.

        Returns the Windows HID call duration in milliseconds.
        """
        self._ensure_open()

        if len(report) != REPORT_SIZE:
            raise ValueError(
                f"Expected {REPORT_SIZE}-byte report, "
                f"got {len(report)} bytes."
            )

        buffer = (
            ctypes.c_ubyte * len(report)
        )(*report)

        start = time.perf_counter()

        ok = HidD_SetOutputReport(
            self._handle,
            ctypes.cast(
                buffer,
                wintypes.LPVOID,
            ),
            len(report),
        )

        elapsed_ms = (
            time.perf_counter() - start
        ) * 1000.0

        if not ok:
            error = ctypes.get_last_error()

            if error:
                raise ctypes.WinError(error)

            raise RuntimeError(
                "HidD_SetOutputReport returned FALSE."
            )

        return elapsed_ms

    def send_reports(self, reports) -> float:
        """
        Send one complete transaction.

        The inter-report gap occurs only between reports, matching
        the previously validated implementation.
        """
        self._ensure_open()

        start = time.perf_counter()

        for index, report in enumerate(reports):
            self.send_report(report)

            if index != len(reports) - 1:
                if self.gap_ms > 0:
                    time.sleep(
                        self.gap_ms / 1000.0
                    )

        return (
            time.perf_counter() - start
        ) * 1000.0

    def close(self):
        if self._closed:
            return

        CloseHandle(self._handle)

        self._handle = None
        self._closed = True

    def __enter__(self):
        self.open()
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        self.close()