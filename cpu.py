# Author: Chase Smith
# GitHub: ChaseSmith67


class CPU(object):

    def __init__(self):
        # 8-Bit Registers: A, X & Y
        self.reg_A = None   # Accumulator
        self.reg_X = None   # X Index
        self.reg_Y = None   # Y Index

        # TODO: consider implementing these as an array?
        # P-Register - 1-Bit Flags
        self.flag_N = None
        self.flag_V = None
        self.flag_B = None
        self.flag_D = None
        self.flag_I = None
        self.flag_Z = None
        self.flag_C = None

        # 8-Bit Stack Pointer
        self.pointer = None

        # 16-Bit Program Counter
        self.counter = None
