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
        self.pointer = np.array([0xFF], dtype=np.uint8)

        # 16-Bit Program Counter
        self.counter = np.array([0, 0], dtype=np.uint8)

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

    def store_reg_in_mem(self, register: np.array, address: int | np.uint) -> None:
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

    def change_flag(self, flag: np.array, value=None) -> None:
        """Changes the Boolean value of the specified flag to the specified value. If no
            value is given, the flag's state will be changed."""
        if value is None:
            flag[0] = not flag[0]
        else:
            flag[0] = value

    # ----- Below this line: Instructions - May move these to a separate file later.
    # ----- Having these individually like this isn't strictly necessary, may refactor.

    def AND(self, address: int | np.uint) -> None:
        """Bitwise Memory AND Accumulator, Result stored in Accumulator"""
        mem_val = mem.read_mem(address)
        a_val = self.read_reg(self.reg_A)
        result = mem_val & a_val
        self.write_reg(self.reg_A, result)
        self.change_flag(self.flag_Z, (result == 0))

    def LDA(self, address: int | np.uint) -> None:
        """Load Accumulator from specified Memory address"""
        self.load_reg_from_mem(self.reg_A, address)

    def LDX(self, address: int | np.uint) -> None:
        """Load Index X from specified Memory address"""
        self.load_reg_from_mem(self.reg_X, address)

    def LDY(self, address: int | np.uint) -> None:
        """Load Index Y from specified Memory address"""
        self.load_reg_from_mem(self.reg_Y, address)

    def LSR(self, location) -> None:
        """Logical Shift Right by One Bit. Least significant bit stored in Carry Flag.
            Specified location can be either a Memory address or Accumulator."""
        if type(location) == np.ndarray:
            value = self.reg_A[0]
            self.change_flag(self.flag_C, (value % 2))
            self.write_reg(self.reg_A, (value >> 1))
        else:
            value = self.memory.read_mem(location)
            self.change_flag(self.flag_C, (value % 2))
            self.memory.write_mem(location, (value >> 1))



class Memory(object):
    """
    Represents the memory to be utilized by the CPU. Consists of a 2D array of 8 pages
    of 256 elements each, with each element being 1 byte.
    ** NOTE: Little Endian **
    """
    def __init__(self):
        self.memory = np.zeros(shape=(8, 256), dtype=np.uint8)

    def get_memory(self) -> np.array:
        """Returns entire memory array"""
        return self.memory

    def read_mem(self, address: int | np.uint16) -> np.uint8:
        """Returns the data stored at the specified position in the memory array"""

        low_byte = address.to_bytes(2, "little")[0]
        high_byte = address.to_bytes(2, "little")[1]

        return self.memory[high_byte][low_byte]

    def write_mem(self, address: int | np.uint16, value: int | np.uint8) -> None:
        """Sets the specified position in the memory array equal to the given value"""

        low_byte = address.to_bytes(2, "little")[0]
        high_byte = address.to_bytes(2, "little")[1]

        self.memory[high_byte][low_byte] = value


# ========  Below this line is temporary functionality testing  =========

mem = Memory()
cpu = CPU(mem)
a, x, y = cpu.reg_A, cpu.reg_X, cpu.reg_Y
n, v, b, d, i, z, c = cpu.flag_N, cpu.flag_V, cpu.flag_B, cpu.flag_D, cpu.flag_I, cpu.flag_Z, cpu.flag_C


# # LDA #$01  - load literal 0x01 into accumulator
# cpu.write_reg(a, 0x01)
# # STA $0200 - store accumulator value in 0x0200
# cpu.store_reg_in_mem(a, 0x00)
# # LDA #$05  - load literal 0x05 into accumulator
# cpu.write_reg(a, 0x05)
# # STA $0201 - store accumulator value in 0x0201
# cpu.store_reg_in_mem(a, 0x01)
# # LDA #$08  - load literal 0x08 into accumulator
# cpu.write_reg(a, 0x08)
# # STA $0202 - store accumulator value in 0x0202
# cpu.store_reg_in_mem(a, 0x02)
#
# print(mem.read_mem(0x00))
# print(mem.read_mem(0x01))
# print(mem.read_mem(0x02))

print("REG LSR")
cpu.write_reg(a, 0x021)
print(cpu.read_reg(a))
cpu.LSR(a)
print(cpu.read_reg(a))

print("MEM LSR")
mem.write_mem(0x05, 0x0A)
print(mem.read_mem(0x05))
cpu.LSR(0x05)
print(mem.read_mem(0x05))
print(cpu.read_flag(cpu.flag_Z))
print("AND")
cpu.AND(0x05)
print(cpu.read_reg(a))
print(cpu.read_flag(cpu.flag_Z))

