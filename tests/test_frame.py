import pytest

from rkm75 import Frame
from rkm75.protocol import LED_COUNT


def test_frame_starts_black():
    frame = Frame()

    assert len(frame.bytes) == LED_COUNT * 3
    assert frame.bytes == bytes(LED_COUNT * 3)


def test_fill_sets_all_leds():
    frame = Frame()

    frame.fill((255, 0, 0))

    assert frame.bytes == bytes((255, 0, 0)) * LED_COUNT


def test_set_led():
    frame = Frame()

    frame.set_led(0, (1, 2, 3))

    assert frame.bytes[:3] == bytes((1, 2, 3))


def test_set_last_led():
    frame = Frame()

    frame.set_led(LED_COUNT - 1, (1, 2, 3))

    assert frame.bytes[-3:] == bytes((1, 2, 3))


def test_set_led_rejects_out_of_range_index():
    frame = Frame()

    with pytest.raises(IndexError):
        frame.set_led(LED_COUNT, (1, 2, 3))


def test_set_led_rejects_negative_index():
    frame = Frame()

    with pytest.raises(IndexError):
        frame.set_led(-1, (1, 2, 3))


def test_set_led_rejects_invalid_color_length():
    frame = Frame()

    with pytest.raises(ValueError):
        frame.set_led(0, (255, 0))


def test_set_led_rejects_non_integer_color():
    frame = Frame()

    with pytest.raises(ValueError):
        frame.set_led(0, (255, 0, 1.5))


def test_set_led_rejects_boolean_color():
    frame = Frame()

    with pytest.raises(ValueError):
        frame.set_led(0, (True, False, True))


def test_set_led_rejects_out_of_range_color():
    frame = Frame()

    with pytest.raises(ValueError):
        frame.set_led(0, (256, 0, 0))


def test_set_key():
    frame = Frame()

    frame.set_key("A", (1, 2, 3))

    assert frame.bytes[9 * 3:9 * 3 + 3] == bytes((1, 2, 3))


def test_set_key_is_case_insensitive():
    frame = Frame()

    frame.set_key("a", (1, 2, 3))

    assert frame.bytes[9 * 3:9 * 3 + 3] == bytes((1, 2, 3))


def test_set_key_rejects_unknown_key():
    frame = Frame()

    with pytest.raises(KeyError, match="Unknown key"):
        frame.set_key("NOT_A_KEY", (1, 2, 3))