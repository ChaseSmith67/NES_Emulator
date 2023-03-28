# Author: Chase Smith
# GitHub username: ChaseSmith67
# Date: 3/26/23
# Description: Emulation of the 6502 microprocessor and its instruction set.

import numpy as np



class CPU(object):

    def __init__(self, ram):
        """
        Initializes the CPU object and sets all registers and flags to 0.
        Creates RAM necessary for operation.
        """

        # Create RAM
        self.ram = ram

        # 8-Bit Registers: A, X & Y
        self.reg_A = np.array([0], dtype=np.uint8)  # Accumulator Register
        self.reg_X = np.array([0], dtype=np.uint8)  # Index Register X
        self.reg_Y = np.array([0], dtype=np.uint8)  # Index Register Y

        # Considering implementing these as an array...
        # P-Register - 1-Bit Flags
        self.flag_N = np.bool_(0)    # Negative Flag
        self.flag_V = np.bool_(0)    # Overflow
        self.flag_B = np.bool_(0)    # Break Command
        self.flag_D = np.bool_(0)    # Decimal Mode Flag
        self.flag_I = np.bool_(0)    # Interrupt Disable
        self.flag_Z = np.bool_(0)    # Zero Flag
        self.flag_C = np.bool_(0)    # Carry Flag

        # 8-Bit Stack Pointer
        self.pointer = np.uint8(0)

        # 16-Bit Program Counter
        self.counter = np.uint16(0)

    def load_reg_from_mem(self, register: np):
        pass

    def read_reg(self, register: np.array) -> np.uint8:
        return register[0]

    def write_reg(self, register: np.array, value: int) -> None:
        register[0] = np.uint8(value)

    def increment(self, register: np.uint8) -> None:
        register += np.uint8(1)


class RAM(object):
    """
    Represents the Random Access Memory to be utilized by the CPU. Consists of
    an array of bytes. Takes as a parameter the desired memory size in KB.
    """
    def __init__(self, size: int):
        self.memory = np.array([0] * (size * 1024), dtype=np.uint8)

    def get_memory(self) -> np.array(np.uint8):
        """Returns entire memory array"""
        return self.memory

    def read_mem(self, address: int) -> np.uint8:
        """Returns the data stored at the specified position in the memory array.
            *Note: Each element in the array represents a byte, so address is divided by 8."""
        return self.memory[address // 8]

    def write_mem(self, address: int, value: np.uint8) -> None:
        """Sets the specified position in the memory array equal to the given value
            *Note: Each element in the array represents a byte, so address is divided by 8."""
        self.memory[address // 8] = value


# ========  Below this line is temporary functionality testing  =========

ram = RAM(2)
cpu = CPU(ram)

print(cpu.reg_X)

print(cpu.read_reg(cpu.reg_X))

cpu.write_reg(cpu.reg_X, 0x0A)

print(cpu.reg_X)

print(cpu.read_reg(cpu.reg_X))



