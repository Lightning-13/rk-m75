from rkm75.device import RKM75Device


def test_constants():
    assert RKM75Device.VID == 0x258A
    assert RKM75Device.PID == 0x0163
    assert RKM75Device.INTERFACE == 1