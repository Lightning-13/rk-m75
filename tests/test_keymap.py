from rkm75.keymap import KEYMAP


def test_keymap_has_81_keys():
    assert len(KEYMAP) == 81


def test_keymap_contains_expected_keys():
    expected_keys = {
        "ESC",
        "TAB",
        "CAPS_LOCK",
        "LEFT_SHIFT",
        "LEFT_CTRL",
        "LEFT_ALT",
        "SPACE",
        "ENTER",
        "BACKSPACE",
        "A",
        "Z",
        "M",
        "0",
        "9",
        "HOME",
        "PAGE_UP",
        "PAGE_DOWN",
        "UP",
        "LEFT",
        "DOWN",
        "RIGHT",
    }

    assert expected_keys <= KEYMAP.keys()


def test_keymap_indices_are_unique():
    indices = list(KEYMAP.values())

    assert len(indices) == len(set(indices))


def test_keymap_indices_are_non_negative():
    assert all(index >= 0 for index in KEYMAP.values())


def test_validated_key_positions():
    assert KEYMAP["A"] == 9
    assert KEYMAP["SPACE"] == 35