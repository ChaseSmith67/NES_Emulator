# Author: Chase Smith
# GitHub: ChaseSmith67


import argparse
import numpy as np

# from cpu import CPU
from ram import RAM
from instructions import instructions


class System(object):
    """
    Represents the complete computing system, with all necessary components.
    """
    def __init__(self):
        self.ram = RAM()
        self.cpu = CPU(self.ram)


def system_setup() -> System:
    NES = System()

    return NES


def parse_args() -> object:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", "-p", type=str, help="Path to ROM file")
    # TODO: set up default ROM path, so user only enters ROM title

    args = parser.parse_args()

    return args


def main():

    # === SETUP TO READ ROM
    # args = parse_args()
    #
    # # TODO: validate ROM path
    # rom_path = args.path
    #
    # print(rom_path)
    #
    # with open(rom_path, "rb") as file:
    #     for line in file.readlines():
    #         print(line)

    system = system_setup()

    reg_x = system.cpu.reg_X

    print(reg_x)

    system.cpu.set_reg_X(system.cpu.get_reg_X()+np.uint8(1))

    print(system.cpu.get_reg_X())




if __name__ == "__main__":
    main()



