# Author: Chase Smith
# GitHub username: ChaseSmith67
# Date: 3/26/23
# Description: Emulation of the 6502 microprocessor and its instruction set.

import numpy as np



class CPU(object):
    """
    Represents the 6502 processor. Has 8-bit arrays representing the registers
    and stack pointer, 1-bit arrays representing the flags, a 16-bit array
    representing the program counter, and a Memory Object that is used to emulate
    the 2KB of memory for storing data, including the stack.
    """
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
        self.SP = np.array([0xFF], dtype=np.uint8)

        # 16-Bit Program Counter
        self.PC = np.array([0, 0], dtype=np.uint8)

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

    def read_flag(self, flag: np.array) -> np.bool_:
        """Returns the Boolean value of the specified flag"""
        return flag[0]

    def change_flag(self, flag: np.array, value=None) -> None:
        """Changes the Boolean value of the specified flag to the specified value. If no
            value is given, the flag's state will be changed."""
        if value is None:
            flag[0] = not flag[0]
        else:
            flag[0] = value

    def get_processor_status(self) -> np.uint8:
        """Returns the current status of the flags as an 8-bit value. The Break Flag and
            bit 5 are both set to 1"""
        # Read flags in order
        status = np.array([0, 0, 1, 1, 0, 0, 0, 0], dtype=np.bool_)
        status[0] = self.read_flag(self.flag_N)
        status[1] = self.read_flag(self.flag_V)
        status[4] = self.read_flag(self.flag_D)
        status[5] = self.read_flag(self.flag_I)
        status[6] = self.read_flag(self.flag_Z)
        status[7] = self.read_flag(self.flag_C)
        # Reverse flag array and convert to 8-bit integer
        bits = status[::-1]
        result = np.sum(np.logspace(0, bits.size - 1, num=bits.size, base=2) * bits, dtype=np.int8)
        return result.view(dtype=np.uint8)

    # ----- Below this line: Instructions - May move these to a separate file later.
    # ----- Having these individually like this isn't strictly necessary, may refactor.
    # TODO: Negative values don't work yet. Determine best way to implement.
    # TODO: Addressing Modes haven't been accounted for yet.

    def AND(self, address: int | np.uint) -> None:
        """Bitwise Memory AND Accumulator, Result stored in Accumulator. If the result is
         Zero or Negative, the appropriate flag will be set."""
        mem_val = self.memory.read_mem(address)
        a_val = self.read_reg(self.reg_A)
        result = mem_val & a_val
        self.write_reg(self.reg_A, result)
        self.change_flag(self.flag_Z, (result == 0))
        self.change_flag(self.flag_N, (result < 0))

    def ASL(self, location) -> None:
        """Arithmatic Shift Left by One Bit. Most significant bit (Bit 7) is stored in
            Carry Flag. Specified location can be either Memory address or Accumulator"""
        if type(location) == np.ndarray:
            value = self.read_reg(self.reg_A)
            self.write_reg(self.reg_A, (value << 1))
        else:
            value = self.memory.read_mem(location)
            self.memory.write_mem(location, (value << 1))
        self.change_flag(self.flag_C, (value >= 128))

    def CLC(self) -> None:
        """Clear Carry Flag"""
        self.change_flag(self.flag_C, 0)

    def CLD(self) -> None:
        """Clear Decimal Mode Flag"""
        self.change_flag(self.flag_D, 0)

    def CLI(self) -> None:
        """Clear Interrupt Disable Flag"""
        self.change_flag(self.flag_I, 0)

    def CLV(self) -> None:
        """Clear Overflow Flag"""
        self.change_flag(self.flag_V, 0)

    def CMP(self, address: int | np.uint) -> None:
        """Compare Accumulator with Memory. If the value of the Accumulator is greater
            than or equal to the value at the given Memory address, the Carry flag will
            be set. If Accumulator is Zero or Negative, those flags will be set as well."""
        mem_val = self.memory.read_mem(address)
        a_val = self.read_reg(self.reg_A)
        self.change_flag(self.flag_C, (a_val >= mem_val))
        self.change_flag(self.flag_Z, (a_val == 0))
        self.change_flag(self.flag_N, (a_val < 0))

    def CPX(self, address: int | np.uint) -> None:
        """Compare Index X with Memory. If the value of Index X is greater than or equal to
            the value at the given Memory address, the Carry flag will be set. If Index X
            is Zero or Negative, those flags will be set as well."""
        mem_val = self.memory.read_mem(address)
        x_val = self.read_reg(self.reg_X)
        self.change_flag(self.flag_C, (x_val >= mem_val))
        self.change_flag(self.flag_Z, (x_val == 0))
        self.change_flag(self.flag_N, (x_val < 0))

    def CPY(self, address: int | np.uint) -> None:
        """Compare Index Y with Memory. If the value of Index Y is greater than or equal to
            the value at the given Memory address, the Carry flag will be set. If Index Y
            is Zero or Negative, those flags will be set as well."""
        mem_val = self.memory.read_mem(address)
        y_val = self.read_reg(self.reg_Y)
        self.change_flag(self.flag_C, (y_val >= mem_val))
        self.change_flag(self.flag_Z, (y_val == 0))
        self.change_flag(self.flag_N, (y_val < 0))

    def DEC(self, address: int | np.uint) -> None:
        """Decrement Memory. The value stored at the specified Memory address is decremented
            by 1. If the result is Zero or Negative, the appropriate flag will be set."""
        mem_val = self.memory.read_mem(address)
        mem_val -= 1
        self.change_flag(self.flag_Z, (mem_val == 0))
        self.change_flag(self.flag_N, (mem_val < 0))
        self.memory.write_mem(address, mem_val)

    def DEX(self) -> None:
        """Decrement Index X. The value stored Index Register X is decremented by 1.
            If the result is Zero or Negative, the appropriate flag will be set."""
        val = self.read_reg(self.reg_X)
        val -= 1
        self.write_reg(self.reg_X, val)
        self.change_flag(self.flag_Z, (val == 0))
        self.change_flag(self.flag_N, (val < 0))

    def DEY(self) -> None:
        """Decrement Index Y. The value stored Index Register Y is decremented by 1.
            If the result is Zero or Negative, the appropriate flag will be set."""
        val = self.read_reg(self.reg_Y)
        val -= 1
        self.write_reg(self.reg_Y, val)
        self.change_flag(self.flag_Z, (val == 0))
        self.change_flag(self.flag_N, (val < 0))

    def EOR(self, address: int | np.uint) -> None:
        """Bitwise Exclusive OR Memory with Accumulator. The value stored at the specified
            memory address is compared with the value in the Accumulator using Exclusive OR
            operation and the result is stored in the Accumulator. If the result is Zero or
            Negative, the appropriate flag will be set."""
        mem_val = self.memory.read_mem(address)
        a_val = self.read_reg(self.reg_A)
        result = mem_val ^ a_val
        self.write_reg(self.reg_A, result)
        self.change_flag(self.flag_Z, (result == 0))
        self.change_flag(self.flag_N, (result < 0))

    def INC(self, address: int | np.uint) -> None:
        """Increment Memory. The value stored at the specified Memory address is incremented
            by 1. If the result is Zero or Negative, the appropriate flag will be set."""
        mem_val = self.memory.read_mem(address)
        mem_val += 1
        self.change_flag(self.flag_Z, (mem_val == 0))
        self.change_flag(self.flag_N, (mem_val < 0))
        self.memory.write_mem(address, mem_val)

    def INX(self) -> None:
        """Increment Index X. The value stored Index Register X is incremented by 1.
            If the result is Zero or Negative, the appropriate flag will be set."""
        val = self.read_reg(self.reg_X)
        val += 1
        self.write_reg(self.reg_X, val)
        self.change_flag(self.flag_Z, (val == 0))
        self.change_flag(self.flag_N, (val < 0))

    def INY(self) -> None:
        """Increment Index Y. The value stored Index Register Y is incremented by 1.
            If the result is Zero or Negative, the appropriate flag will be set."""
        val = self.read_reg(self.reg_Y)
        val += 1
        self.write_reg(self.reg_Y, val)
        self.change_flag(self.flag_Z, (val == 0))
        self.change_flag(self.flag_N, (val < 0))

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
            value = self.read_reg(self.reg_A)
            self.write_reg(self.reg_A, (value >> 1))
        else:
            value = self.memory.read_mem(location)
            self.memory.write_mem(location, (value >> 1))
        self.change_flag(self.flag_C, (value % 2))

    def NOP(self) -> None:
        """No Operation. Probably not necessary."""
        pass

    def ORA(self, address: int | np.uint) -> None:
        """Bitwise OR Memory with Accumulator. The value stored at the specified memory
            address is compared with the value in the Accumulator using  OR operation
            and the result is stored in the Accumulator. If the result is Zero or Negative,
            the appropriate flag will be set."""
        mem_val = self.memory.read_mem(address)
        a_val = self.read_reg(self.reg_A)
        result = mem_val | a_val
        self.write_reg(self.reg_A, result)
        self.change_flag(self.flag_Z, (result == 0))
        self.change_flag(self.flag_N, (result < 0))

    def PHA(self) -> None:
        """Push Accumulator to Stack. Takes the value currently stored in the Accumulator
            Register and stores it in the Memory address currently pointed to by the Stack
            Pointer. Stack Pointer decremented."""
        address = int(0x0100 + self.read_reg(self.SP))
        self.memory.write_mem(address, (self.read_reg(self.reg_A)))
        self.decrement(self.SP)

    def PHP(self) -> None:
        """Push Processor Status to Stack. Takes the values of all flags, represented as
            an 8-bit integer and stores it in the Memory address currently pointed to by
            the Stack Pointer. Stack Pointer decremented."""
        address = int(0x0100 + self.read_reg(self.SP))
        status = self.get_processor_status()
        self.memory.write_mem(address, status)
        self.decrement(self.SP)

    def PLA(self) -> None:
        """Pull Accumulator from Stack. The value in the Memory address pointed to by the
            Stack Pointer is stored in the Accumulator. Stack Pointer incremented"""
        self.increment(self.SP)
        address = int(0x0100 + self.read_reg(self.SP))
        value = self.memory.read_mem(address)
        self.write_reg(self.reg_A, value)

    def PLP(self) -> None:
        """Pull Processor Status from Stack. The value in the Memory address pointed to by the
            Stack Pointer is pulled and the Status Flags set accordingly. Stack Pointer incremented"""
        self.increment(self.SP)
        address = int(0x0100 + self.read_reg(self.SP))
        value = str(bin(self.memory.read_mem(address)))
        bits = value[2:]
        while len(bits) < 8:    # This is kinda janky, will likely refactor later
            bits = "0" + bits
        self.change_flag(self.flag_N, (bits[0] != 0))
        self.change_flag(self.flag_V, (bits[1] != 0))
        self.change_flag(self.flag_D, (bits[4] != 0))
        self.change_flag(self.flag_I, (bits[5] != 0))
        self.change_flag(self.flag_Z, (bits[6] != 0))
        self.change_flag(self.flag_C, (bits[7] != 0))

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
        address = int(address)

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


cpu.memory.write_mem(0x05, 0x05)
print(mem.read_mem(0x05))
print(cpu.read_reg(a))
cpu.LDA(0x05)
print(cpu.read_reg(a))
print(cpu.memory.read_mem(0x01FF))
cpu.PHA()
print(cpu.memory.read_mem(0x01FF))
print(cpu.read_reg(cpu.SP))
print(cpu.memory.read_mem(cpu.read_reg(cpu.SP)))

print(cpu.get_processor_status())
cpu.PHP()
print(cpu.memory.read_mem(0x01FE))
print(cpu.read_reg(cpu.SP))
print(cpu.memory.read_mem(cpu.read_reg(cpu.SP)))
cpu.PLP()

