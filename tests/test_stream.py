import pytest

from rkm75 import RGBStream


class FakeDevice:
    def __init__(self):
        self.frames = []

    def send(self, frame):
        self.frames.append(frame)


def test_default_fps():
    stream = RGBStream(FakeDevice())

    assert stream.fps == 33.0
    assert stream.interval == pytest.approx(1 / 33)


def test_valid_fps():
    stream = RGBStream(FakeDevice(), fps=10)

    assert stream.fps == 10
    assert stream.interval == pytest.approx(0.1)


@pytest.mark.parametrize("fps", [0, -1])
def test_rejects_non_positive_fps(fps):
    with pytest.raises(ValueError, match="greater than 0"):
        RGBStream(FakeDevice(), fps=fps)


@pytest.mark.parametrize("fps", [34, 100])
def test_rejects_fps_above_maximum(fps):
    with pytest.raises(ValueError, match="must not exceed 33"):
        RGBStream(FakeDevice(), fps=fps)


@pytest.mark.parametrize(
    "fps",
    [float("nan"), float("inf"), float("-inf"), "33", None, True, False],
)
def test_rejects_invalid_fps_types_and_values(fps):
    with pytest.raises(ValueError, match="finite number"):
        RGBStream(FakeDevice(), fps=fps)


def test_stream_requires_context_manager():
    stream = RGBStream(FakeDevice())

    with pytest.raises(
        RuntimeError,
        match="must be used as a context manager",
    ):
        stream.send(object())


def test_stream_context_lifecycle():
    stream = RGBStream(FakeDevice())

    assert stream._next_send is None

    with stream as active:
        assert active is stream
        assert stream._next_send is not None

    assert stream._next_send is None


def test_stream_sends_frame():
    device = FakeDevice()
    frame = object()

    with RGBStream(device, fps=33) as stream:
        stream.send(frame)

    assert device.frames == [frame]