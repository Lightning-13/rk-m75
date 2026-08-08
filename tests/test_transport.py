import pytest

from rkm75.transport import HidTransport


class FakeHIDDevice:
    def __init__(self):
        self.closed = False
        self.sent_reports = []
        self.close_calls = 0

    def open_path(self, path):
        self.path = path

    def send_feature_report(self, report):
        self.sent_reports.append(report)
        return len(report)

    def get_feature_report(self, report_id, length):
        return [report_id] + [0] * (length - 1)

    def close(self):
        self.close_calls += 1
        self.closed = True


def make_transport(monkeypatch):
    device = FakeHIDDevice()

    class FakeHIDModule:
        @staticmethod
        def device():
            return device

    monkeypatch.setattr("rkm75.transport.hid", FakeHIDModule)

    transport = HidTransport(b"test-path")

    return transport, device


def test_transport_starts_open(monkeypatch):
    transport, device = make_transport(monkeypatch)

    assert transport._closed is False
    assert device.path == b"test-path"


def test_send_feature_requires_520_bytes(monkeypatch):
    transport, _ = make_transport(monkeypatch)

    with pytest.raises(ValueError, match="520-byte"):
        transport.send_feature(b"\x00")


def test_send_feature(monkeypatch):
    transport, device = make_transport(monkeypatch)
    report = bytes(520)

    result = transport.send_feature(report)

    assert result == 520
    assert device.sent_reports == [report]


def test_get_feature(monkeypatch):
    transport, _ = make_transport(monkeypatch)

    result = transport.get_feature(9, 4)

    assert result == bytes([9, 0, 0, 0])


def test_close_closes_device(monkeypatch):
    transport, device = make_transport(monkeypatch)

    transport.close()

    assert transport._closed is True
    assert device.closed is True
    assert device.close_calls == 1


def test_close_is_idempotent(monkeypatch):
    transport, device = make_transport(monkeypatch)

    transport.close()
    transport.close()

    assert transport._closed is True
    assert device.close_calls == 1


def test_send_after_close_is_rejected(monkeypatch):
    transport, _ = make_transport(monkeypatch)

    transport.close()

    with pytest.raises(RuntimeError, match="HID transport is closed"):
        transport.send_feature(bytes(520))


def test_get_after_close_is_rejected(monkeypatch):
    transport, _ = make_transport(monkeypatch)

    transport.close()

    with pytest.raises(RuntimeError, match="HID transport is closed"):
        transport.get_feature(9, 520)