# Author: Chase Smith
# GitHub: ChaseSmith67


import argparse


def parse_args() -> object:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", "-p", type=str, help="Path to ROM file")

    args = parser.parse_args()

    return args


def main():
    args = parse_args()
    rom_path = args.path

    print(rom_path)



if __name__ == "__main__":
    main()