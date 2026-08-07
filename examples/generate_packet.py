from rkm75 import Frame
from rkm75.packet import Packet

frame = Frame()

# Fill every LED slot with red
frame.fill((255, 0, 0))

packet = Packet(frame)

packet.save("generated.bin")

print("Generated packet:", len(packet.to_bytes()), "bytes")