import hid
from pprint import pprint

for d in hid.enumerate():
    if d["vendor_id"] == 0x258A and d["product_id"] == 0x0163:
        print("=" * 80)
        pprint(d)