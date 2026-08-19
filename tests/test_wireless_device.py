from rkm75.wireless.device import RKM75Wireless
import pytest

def test_wireless_device_requires_open_for_send():
    device = RKM75Wireless()

    try:
        device.send_frame(None)
    except RuntimeError as exc:
        assert "not open" in str(exc).lower()
    else:
        raise AssertionError(
            "Sending before open should fail."
        )


def test_wireless_device_default_gap():
    device = RKM75Wireless()

    assert device.gap_ms == 7.0
    assert device.transport is None

def test_wireless_device_keepalive_requires_open():
    device = RKM75Wireless()

    with pytest.raises(RuntimeError):
        device.send_keepalive()