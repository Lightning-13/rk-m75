from pathlib import Path

from rkm75.packet import Packet
from rkm75.protocol import (
    FRAME_SIZE,
    HEADER,
    PADDING_SIZE,
    REPORT_SIZE,
)


class FakeFrame:
    def __init__(self, data):
        self.bytes = bytes(data)


def test_packet_size():
    frame = FakeFrame(bytes(FRAME_SIZE))

    packet = Packet(frame)

    assert len(packet.to_bytes()) == REPORT_SIZE


def test_packet_starts_with_header():
    frame = FakeFrame(bytes(FRAME_SIZE))

    packet = Packet(frame)

    data = packet.to_bytes()

    assert data[:len(HEADER)] == HEADER


def test_packet_contains_frame():
    frame_data = bytes((i % 256 for i in range(FRAME_SIZE)))

    frame = FakeFrame(frame_data)
    packet = Packet(frame)

    data = packet.to_bytes()

    start = len(HEADER)
    end = start + FRAME_SIZE

    assert data[start:end] == frame_data


def test_packet_ends_with_padding():
    frame = FakeFrame(bytes(FRAME_SIZE))

    packet = Packet(frame)

    data = packet.to_bytes()

    assert data[-PADDING_SIZE:] == bytes(PADDING_SIZE)


def test_packet_layout():
    frame_data = bytes((i % 256 for i in range(FRAME_SIZE)))

    frame = FakeFrame(frame_data)
    packet = Packet(frame)

    data = packet.to_bytes()

    assert data == (
        HEADER
        + frame_data
        + bytes(PADDING_SIZE)
    )


def test_packet_save(tmp_path: Path):
    frame = FakeFrame(bytes(FRAME_SIZE))
    packet = Packet(frame)

    filename = tmp_path / "packet.bin"
    packet.save(filename)

    assert filename.read_bytes() == packet.to_bytes()
    assert filename.stat().st_size == REPORT_SIZE