# Author: Chase Smith
# GitHub: ChaseSmith67


import argparse


def parse_args() -> object:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", "-p", type=str, help="Path to ROM file")
    # TODO: set up default ROM path, so user only enters ROM title

    args = parser.parse_args()

    return args


def main():
    args = parse_args()

    # TODO: validate ROM path
    rom_path = args.path

    print(rom_path)

    with open(rom_path, "rb") as file:
        for line in file.readlines():
            print(line)


if __name__ == "__main__":
    main()