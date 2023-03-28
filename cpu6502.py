# Author: Chase Smith
# GitHub username: ChaseSmith67
# Date: 3/26/23
# Description: Emulation of the 6502 microprocessor and its instruction set.

import numpy as np



class CPU(object):

    def __init__(self, memory):
        """
        Initializes the CPU object and sets all registers and flags to 0.
        Creates Memory necessary for operation.
        """

        # Create Memory
        self.memory = memory

        # 8-Bit Registers: A, X & Y
        self.reg_A = np.array([0], dtype=np.uint8)  # Accumulator Register
        self.reg_X = np.array([0], dtype=np.uint8)  # Index Register X
        self.reg_Y = np.array([0], dtype=np.uint8)  # Index Register Y

        # Considering implementing these as an array...
        # P-Register - 1-Bit Flags
        self.flag_N = np.array([0], dtype=np.bool_)    # Negative Flag
        self.flag_V = np.array([0], dtype=np.bool_)    # Overflow
        self.flag_B = np.array([0], dtype=np.bool_)    # Break Command
        self.flag_D = np.array([0], dtype=np.bool_)    # Decimal Mode Flag
        self.flag_I = np.array([0], dtype=np.bool_)    # Interrupt Disable
        self.flag_Z = np.array([0], dtype=np.bool_)    # Zero Flag
        self.flag_C = np.array([0], dtype=np.bool_)    # Carry Flag

        # 8-Bit Stack Pointer
        self.pointer = np.array([0x00FF], dtype=np.uint8)

        # 16-Bit Program Counter
        self.counter = np.array([0x0800], dtype=np.uint16)

    def read_reg(self, register: np.array) -> np.uint8:
        """Returns the 8-bit value stored in the specified register."""
        return register[0]

    def write_reg(self, register: np.array, value: int | np.uint8) -> None:
        """Takes an integer value and stores it in the specified register."""
        register[0] = np.uint8(value)

    def load_reg_from_mem(self, register: np.array, address: int) -> None:
        """Takes the 8-bit value from the specified memory address and stores it
            in the specified register."""
        register[0] = self.memory.read_mem(address)

    def store_reg_in_mem(self, register: np.array, address: int) -> None:
        """Loads the value stored in the specified register into the given memory address"""
        self.memory.write_mem(address, self.read_reg(register))

    def increment(self, register: np.array, amount: int | np.uint8 = 1) -> None:
        """Decrement the value stored in the specified register. Optional amount can be
            specified, default is 1."""
        register[0] += amount

    def decrement(self, register: np.array, amount: int | np.uint8 = 1) -> None:
        """Decrement the value stored in the specified register. Optional amount can be
            specified, default is 1."""
        register[0] -= amount

    def read_flag(self, flag: np.array) -> None:
        """Returns the Boolean value of the specified flag"""
        return flag[0]

    def change_flag(self, flag: np.array) -> None:
        """Changes the Boolean value of the specified flag"""
        flag[0] = not flag[0]


class Memory(object):
    """
    Represents the memory to be utilized by the CPU. Consists of a 2D array of 8 pages
    of 256 elements each, with each element being 1 byte.
    """
    def __init__(self):
        self.memory = np.zeros(shape=(8, 256), dtype=np.uint8)
        # Considering breaking memory array into separate components: ZP, Stack, Gen Purpose

    def get_memory(self) -> np.array:
        """Returns entire memory array"""
        return self.memory

    def read_mem(self, address: int) -> np.uint8:
        """Returns the data stored at the specified position in the memory array"""
        return self.memory[address]

    def write_mem(self, address: int, value: int | np.uint8) -> None:
        """Sets the specified position in the memory array equal to the given value"""
        self.memory[address] = value


# ========  Below this line is temporary functionality testing  =========

mem = Memory()
cpu = CPU(mem)
a = cpu.reg_A
x = cpu.reg_X
y = cpu.reg_Y


# LDA #$01  - load literal 0x01 into accumulator
cpu.write_reg(a, 0x01)
# STA $0200 - store accumulator value in 0x0200
cpu.store_reg_in_mem(a, 0x0200)
# LDA #$05  - load literal 0x05 into accumulator
cpu.write_reg(a, 0x05)
# STA $0201 - store accumulator value in 0x0201
cpu.store_reg_in_mem(a, 0x0208)
# LDA #$08  - load literal 0x08 into accumulator
cpu.write_reg(a, 0x08)
# STA $0202 - store accumulator value in 0x0202
cpu.store_reg_in_mem(a, 0x0210)

print(mem.read_mem(0x0200))
print(mem.read_mem(0x0208))
print(mem.read_mem(0x0210))
