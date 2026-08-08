import pytest

from rkm75.device import RKM75


class FakeTransport:
    def __init__(self, path):
        self.path = path
        self.closed = False
        self.sent_reports = []
        self.sent_frames = []

    def send_feature(self, data):
        self.sent_reports.append(data)
        return len(data)

    def close(self):
        self.closed = True


def make_device(monkeypatch):
    fake_transport = FakeTransport(b"test-path")

    def fake_discover():
        return {"path": b"test-path"}

    monkeypatch.setattr("rkm75.device.discover", fake_discover)
    monkeypatch.setattr(
        "rkm75.device.HidTransport",
        lambda path: fake_transport,
    )

    device = RKM75()

    return device, fake_transport


def test_device_initializes_from_discovery(monkeypatch):
    device, transport = make_device(monkeypatch)

    assert device.device_info == {"path": b"test-path"}
    assert transport.path == b"test-path"


def test_send_feature_report(monkeypatch):
    device, transport = make_device(monkeypatch)

    report = bytes(520)

    result = device.send_feature_report(report)

    assert result == 520
    assert transport.sent_reports == [report]


def test_send_delegates_to_transport(monkeypatch):
    device, transport = make_device(monkeypatch)

    frame = object()

    class FakePacket:
        def __init__(self, received_frame):
            assert received_frame is frame

        def to_bytes(self):
            return bytes(520)

    monkeypatch.setattr("rkm75.packet.Packet", FakePacket)

    result = device.send(frame)

    assert result == 520
    assert transport.sent_reports == [bytes(520)]


def test_stream_returns_rgb_stream(monkeypatch):
    device, _ = make_device(monkeypatch)

    stream = device.stream(fps=33)

    assert stream.device is device
    assert stream.fps == 33


def test_close_delegates_to_transport(monkeypatch):
    device, transport = make_device(monkeypatch)

    device.close()

    assert transport.closed is True


def test_context_manager_closes_device(monkeypatch):
    device, transport = make_device(monkeypatch)

    with device as active:
        assert active is device
        assert transport.closed is False

    assert transport.closed is True