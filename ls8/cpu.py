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

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0

    def load(self, program=[]):
        """Load a program into memory."""

        address = 0

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
            multiple = int(self.reg[reg_a], 2) * int(self.reg[reg_b], 2)
            binary = bin(multiple).replace('0b', '')
            while len(binary) < 8:
                binary = '0' + binary
            self.reg[reg_a] = binary
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
    def run(self, params=[]):
    # def run(self, param1=None, param2=None):
        par_c = 0
        # cur_param = param1
        """Run the CPU."""
        while True:
# LDI expects 2 params(regIndex, value)
            if self.ram[self.pc] == 0b10000010: # LDI
                ldi_param_reg = self.ram[self.pc + 1]
                ldi_param_val = bin(int(params[par_c])).replace('0b', '0000')

                par_c += 1

                self.reg[ldi_param_reg] = ldi_param_val

                self.pc += 2
            
            if self.ram[self.pc] == 0b01000111: # PRN
                prn_param_reg = self.ram[self.pc + 1]
                print(int(self.reg[prn_param_reg], 2))

                self.pc += 2

            if self.ram[self.pc] == 0b10100010: # MULT
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.alu('MULT', reg_a, reg_b)

                # print(reg_a)

                self.pc += 3
# HLT
            if self.ram[self.pc] == 0b00000001:
                # self.pc = 0
                break