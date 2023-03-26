# Author: Chase Smith
# GitHub: ChaseSmith67

import numpy as np


class CPU(object):

    def __init__(self):
        # 8-Bit Registers: A, X & Y
        self.reg_A = np.uint8(0)    # Accumulator
        self.reg_X = np.uint8(0)    # X Index
        self.reg_Y = np.uint8(0)    # Y Index

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
