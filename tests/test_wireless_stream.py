from rkm75.frame import Frame
from rkm75.wireless.stream import (
    WirelessKeepalive,
    WirelessRGBStream,
)


class FakeWirelessDevice:
    def __init__(self):
        self.frames = []
        self.keepalives = []

    def send_frame(self, frame):
        self.frames.append(frame)
        return 1.0

    def send_keepalive(self):
        self.keepalives.append(True)
        return 1.0


def make_frame(frame_index):
    frame = Frame()
    frame.fill((frame_index, 0, 0))
    return frame


def test_wireless_rgb_stream_sends_frames():
    device = FakeWirelessDevice()

    stream = WirelessRGBStream(
        device,
        fps=14.0,
    )

    sent = stream.run(
        make_frame,
        duration=0.15,
    )

    assert sent > 0
    assert len(device.frames) == sent
    assert all(
        isinstance(frame, Frame)
        for frame in device.frames
    )


def test_wireless_rgb_stream_rejects_non_frame():
    device = FakeWirelessDevice()

    stream = WirelessRGBStream(
        device,
        fps=14.0,
    )

    def bad_source(frame_index):
        return None

    try:
        stream.run(
            bad_source,
            duration=0.1,
        )
    except TypeError as exc:
        assert "rkm75 Frame" in str(exc)
    else:
        raise AssertionError(
            "Non-Frame source result should be rejected."
        )


def test_wireless_rgb_stream_rejects_excessive_fps():
    device = FakeWirelessDevice()

    try:
        WirelessRGBStream(
            device,
            fps=15.0,
        )
    except ValueError as exc:
        assert "14 FPS" in str(exc)
    else:
        raise AssertionError(
            "FPS above the validated baseline should be rejected."
        )


def test_wireless_keepalive_sends_repeated_keepalives():
    device = FakeWirelessDevice()

    keepalive = WirelessKeepalive(
        device,
        fps=5.0,
    )

    sent = keepalive.run(
        duration=0.45,
    )

    assert sent > 0
    assert len(device.keepalives) == sent


def test_wireless_keepalive_rejects_invalid_duration():
    device = FakeWirelessDevice()

    keepalive = WirelessKeepalive(
        device,
        fps=5.0,
    )

    try:
        keepalive.run(0)
    except ValueError as exc:
        assert "duration" in str(exc)
    else:
        raise AssertionError(
            "Non-positive duration should be rejected."
        )