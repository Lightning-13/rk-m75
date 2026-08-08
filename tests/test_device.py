from rkm75.device import RKM75


def test_device_class():
    assert RKM75 is not None
    assert hasattr(RKM75, "send_feature_report")
    assert hasattr(RKM75, "send")
    assert hasattr(RKM75, "stream")