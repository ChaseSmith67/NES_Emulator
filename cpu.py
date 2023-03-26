# Author: Chase Smith
# GitHub: ChaseSmith67

import numpy as np

# ## Considering several ways of optimizing the way registers are set and
# ## their values retrieved, the abundance of getter/setter methods certainly
# ## clutters things a bit. However, this early in the process, I want them
# ## all separate and easily modified.


class CPU(object):
    """
    Represents the Central Processing Unit, designed to emulate the 6052
    Microprocessor.
    """

    def __init__(self):
        """Initializes the CPU object and sets all registers and flags to 0."""
        # 8-Bit Registers: A, X & Y
        self.reg_A = np.uint8(0)    # Accumulator Register
        self.reg_X = np.uint8(0)    # Index Register X
        self.reg_Y = np.uint8(0)    # Index Register Y

        # TODO: consider implementing these as an array?
        # P-Register - 1-Bit Flags
        self.flag_N = np.bool(0)
        self.flag_V = np.bool(0)
        self.flag_B = np.bool(0)
        self.flag_D = np.bool(0)
        self.flag_I = np.bool(0)
        self.flag_Z = np.bool(0)
        self.flag_C = np.bool(0)

        # 8-Bit Stack Pointer
        self.pointer = np.uint8(0)

        # 16-Bit Program Counter
        self.counter = np.uint16(0)

    def get_reg_A(self) -> np.uint8:
        """Return the 8-bit value stored in Accumulator Register"""
        return self.reg_A

    def set_reg_A(self, val: np.uint8) -> None:
        """Stores the given value in the Accumulator Register"""
        self.reg_A = val

    def get_reg_X(self) -> np.uint8:
        """Return the 8-bit value stored in Index Register X"""
        return self.reg_X

    def set_reg_X(self, val: np.uint8) -> None:
        """Stores the given value in Index Register X"""
        self.reg_X = val

    def get_reg_Y(self) -> np.uint8:
        """Return the 8-bit value stored in Index Register Y"""
        return self.reg_Y

    def set_reg_Y(self, val: np.uint8) -> None:
        """Stores the given value in Index Register Y"""
        self.reg_Y = val

    def get_stack_pointer(self) -> np.uint8:
        """Returns the position of the stack pointer"""

    def set_stack_pointer(self, pos: np.uint8) -> None:
        """Moves the stack pointer to the specified position"""
        self.pointer = pos

    def get_counter(self) -> np.uint16:
        """Returns the value of the Program Counter"""
        return self.counter

    def set_counter(self, val: np.uint16) -> None:
        """Sets the Program Counter to the specified value"""
        self.counter = val

    def get_flag_N(self) -> np.bool:
        return self.flag_N

    def get_flag_V(self) -> np.bool:
        return self.flag_V

    def get_flag_B(self) -> np.bool:
        return self.flag_B

    def get_flag_D(self) -> np.bool:
        return self.flag_D

    def get_flag_I(self) -> np.bool:
        return self.flag_I

    def get_flag_Z(self) -> np.bool:
        return self.flag_Z

    def get_flag_C(self) -> np.bool:
        return self.flag_C


