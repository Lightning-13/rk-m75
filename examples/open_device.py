from rkm75 import RKM75


def main():

    with RKM75() as kb:

        print()

        print("Connected!")

        print()

        for k, v in kb.device_info.items():

            print(f"{k}: {v}")


if __name__ == "__main__":

    main()