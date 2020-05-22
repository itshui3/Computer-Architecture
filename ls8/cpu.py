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
        self.ram = [0] * 0xFF
        self.sp = 0xF4 # Start of the stack
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
            a = int(self.reg[reg_a], 2)
            b = int(self.reg[reg_b], 2)

            summation = a + b
            binary = bin(summation)

            self.reg[reg_a] = binary
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == 'MULT':
            a = int(self.reg[reg_a], 2)
            b = int(self.reg[reg_b], 2)

            multiple = a * b
            binary = bin(multiple)

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
    def run(self):
    # def run(self, param1=None, param2=None):

        # cur_param = param1
        """Run the CPU."""
        while True:
# LDI expects 2 params(regIndex, value)

            if self.ram[self.pc] == 0b10000010: # LDI
                ldi_param_reg = self.ram[self.pc + 1]
                ldi_param_val = self.ram[self.pc + 2]

                # P8 - decimal 8
                # Mult - also dec 8 & 9
                self.reg[ldi_param_reg] = bin(ldi_param_val)
                self.pc += 3
            
            if self.ram[self.pc] == 0b01000111: # PRN
                prn_param_reg = self.ram[self.pc + 1]
                # Check for different types and convert to bin
                # Store everything the same way
                # Store things in forms dependent on what I want to do 
                # print(self.reg[prn_param_reg])
                print(int(self.reg[prn_param_reg], 2))
                self.pc += 2

            if self.ram[self.pc] == 0b10100000: # ADD
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.alu('ADD', reg_a, reg_b)
                self.pc += 3

            if self.ram[self.pc] == 0b10100010: # MULT
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.alu('MULT', reg_a, reg_b)
                self.pc += 3

            if self.ram[self.pc] == 0b01000101:    # PUSH
                self.sp -= 1
                self.ram[self.sp] = self.reg[self.ram[self.pc + 1]]
                self.pc += 2

            if self.ram[self.pc] == 0b01000110:   # POP
                self.reg[self.ram[self.pc + 1]] = self.ram[self.sp]
                self.sp += 1
                self.pc += 2
            
            if self.ram[self.pc] == 0b01010000: # CALL
                # PC + 1 within ram memory is the register
                regIndex = self.ram[self.pc + 1]
                fnIndex = self.reg[regIndex].replace('0b', '')
                # That holds the value of the ram index
                # Which is where the function call begins

                # PUSH bookmark onto stack
                self.sp -= 1
                self.ram[self.sp] = self.pc + 2
                self.pc = int(fnIndex, 2)

            if self.ram[self.pc] == 0b00010001: # RET
                self.pc = self.ram[self.sp] # RET
                self.sp += 1
# HLT
            if self.ram[self.pc] == 0b00000001:
                break

            if self.ram[self.pc] == 0b10100111: # CMP
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]

                if self.reg[reg_a] == self.reg[reg_b]:
                    #set Equal to 1 in LGE, otherwise set to 0
                    print('reg a equal', self.reg[reg_a])
                    print('reg b equal', self.reg[reg_b])
                    pass
                
                if self.reg[reg_a] < self.reg[reg_b]:
                    #set Less-than to 1 in LGE, otherwise set to 0
                    print('reg a less-than', self.reg[reg_a])
                    print('reg b less-than', self.reg[reg_b])
                    pass

                if self.reg[reg_a] > self.reg[reg_b]:
                    # set Greater-than to 1 in LGE, otherwise set to 0
                    print('reg a greater-than', self.reg[reg_a])
                    print('reg b greater-than', self.reg[reg_b])
                    pass

                self.pc += 3

            # print('No command recognized')