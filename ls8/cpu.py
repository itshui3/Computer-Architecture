# Inventory Notes:
#   file contains a class called CPU
#   it has an empty dunder init
#   a load method with some logic inside
#   an alu method that takes 3 params. 'op' 'reg_a', and 'reg_b'
#   alu seems to want to receive 'add' calculations
#   trace method looks like a print specificaally for seeing into current cpu state
#   run doesn't seem indicative of what it's supposed to do

"""CPU functionality."""

import sys

with open('print8.ls8', 'r') as print8:
    for p in print8:
        print(p)

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000, # LDI expects reg in pc+1
            0b00001000, # LDI expects reg in pc+2
            0b01000111, # PRN R0
            0b00000000, # PRN expects a reg in next pc
            0b00000001, # HLT
        ]

        self.pc = address

        for instruction in program:
            self.ram[address] = instruction
            address += 1

        self.trace()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == 'MULT':
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
    
    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        # Do I have to check if it's 1 byte in binary? 
        self.ram[MAR] = MDR

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % ( # What is this string?
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
# LDI expects 2 params(regIndex, value)
            if self.ram[self.pc] == 0b10000010: # LDI
                ldi_param_reg = self.ram[self.pc + 1]
                ldi_param_val = self.ram[self.pc + 2]

                self.reg[ldi_param_reg] = ldi_param_val

                self.pc += 3
            
            if self.ram[self.pc] == 0b01000111: # PRN
                prn_param_reg = self.ram[self.pc + 1]
                print(self.reg[prn_param_reg])

                self.pc += 2
# HLT
            if self.ram[self.pc] == 0b00000001:
                break