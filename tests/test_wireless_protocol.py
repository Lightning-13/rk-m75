from rkm75.wireless.protocol import (
    NATIVE_PAYLOAD_SIZE,
    REPORT_SIZE,
    packetize,
    reconstruct,
    report_count_for_stream,
    validate_transaction,
)


def test_report_count():
    assert report_count_for_stream(bytes(1)) == 1
    assert report_count_for_stream(bytes(14)) == 1
    assert report_count_for_stream(bytes(15)) == 2
    assert report_count_for_stream(bytes(28)) == 2
    assert report_count_for_stream(bytes(29)) == 3
    assert report_count_for_stream(bytes(42)) == 3
    assert report_count_for_stream(bytes(56)) == 4
    assert report_count_for_stream(bytes(70)) == 5
    assert report_count_for_stream(bytes(84)) == 6
    assert report_count_for_stream(bytes(98)) == 7
    assert report_count_for_stream(bytes(105)) == 8
    assert report_count_for_stream(bytes(113)) == 9
    assert report_count_for_stream(bytes(125)) == 9
    assert report_count_for_stream(bytes(126)) == 9
    assert report_count_for_stream(bytes(127)) == 10


def test_report_size_and_reconstruction():
    for length in (1, 14, 15, 28, 42, 56, 70, 84, 98, 105, 113, 125, 126, 127):
        stream = bytes(range(length))

        reports = packetize(stream)

        assert all(len(report) == REPORT_SIZE for report in reports)

        assert reconstruct(reports) == stream

        validate_transaction(stream, reports)


def test_three_report_transaction():
    stream = bytes(range(42))

    reports = packetize(stream)

    assert len(reports) == 3

    for sequence, report in enumerate(reports):
        assert report[0:3] == bytes.fromhex("13 88 03")
        assert report[3] == sequence

    assert reconstruct(reports) == stream


def test_eight_report_transaction():
    stream = bytes(range(105))

    reports = packetize(stream)

    assert len(reports) == 8

    for sequence, report in enumerate(reports):
        assert report[0:3] == bytes.fromhex("13 88 08")
        assert report[3] == sequence

    assert reconstruct(reports) == stream


def test_payload_capacity():
    stream = bytes(range(105))
    reports = packetize(stream)

    for report in reports[:-1]:
        assert report[4] == 0x10 + NATIVE_PAYLOAD_SIZE

    assert reports[-1][4] == 0x10 + 7

def test_129_byte_stream_packetizes_as_13_88_0a():
    stream = bytes(range(129))

    reports = packetize(stream)

    assert len(reports) == 10

    for sequence, report in enumerate(reports):
        assert len(report) == REPORT_SIZE
        assert report[:3] == bytes((0x13, 0x88, 0x0A))
        assert report[3] == sequence

    validate_transaction(stream, reports)

    assert reconstruct(reports) == stream