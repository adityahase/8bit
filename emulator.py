"""
Instruction Set
0x00    NOP BLANK   BLANK
0x10    ADD TARGET  SOURCE
0x20    AND TARGET  SOURCE
0x30    DEC TARGET  BLANK
0x40    DIV TARGET  SOURCE
0x50    INC TARGET  BLANK
0x60    JMP TARGET  BLANK
0x70    JZ  TARGET  BLANK
0x80    MOV TARGET  SOURCE
0x90    MUL TARGET  SOURCE
0xA0    NEG TARGET  BLANK
0xB0    SUB TARGET  SOURCE
0xC0    OR  TARGET  SOURCE
0xD0    XOR TARGET  SOURCE
0xF0    HLT TARGET  SOURCE
"""


OPCODE_MAP = {
    "NOP": 0x00,
    "ADD": 0x10,
    "AND": 0x20,
    "DEC": 0x30,
    "DIV": 0x40,
    "INC": 0x50,
    "JMP": 0x60,
    "JZ": 0x70,
    "MOV": 0x80,
    "MUL": 0x90,
    "NEG": 0xA0,
    "SUB": 0xB0,
    "OR": 0xC0,
    "XOR": 0xD0,
    "HLT": 0xF0
}

REGISTER_MAP = {
    "A": 0xF0,
    "B": 0xF1,
    "SP": 0xF2,
    "PC": 0xF3,
    "R0": 0xF4,
    "R1": 0xF5,
    "R2": 0xF6,
    "R3": 0xF7,
}

OP_MASK_SIMPLE = 0x00
OP_MASK_INDIRECT = 0x01
OP_MASK_DATA = 0x02

MEMORY_SIZE = 256

class Emulator(object):
    def __init__(self, memory, program, registers):
        self.memory = [0]*MEMORY_SIZE
        self.code = []
        for instruction in Assembler(program).assemble():
            self.code.extend(instruction)
        self.memory[:len(self.code)] = self.code

    def run(self):
        for instruction in self.machine_code:
            opcode, operand1, operand2 = instruction
            yield self.state()

    def state(self):
        return {
            "memory": self.memory,
            "registers": self.registers
        }


def Assembler():
    def __init__(self, program):
        self.program = program

    def assemble(self):
        return [self.decode(instruction) for instruction in self.program]

    def decode(self, asm_instruction):
        asm_opcode, *asm_operands = asm_instruction
        machine_opcode = decode_opcode(asm_opcode)
        target, source = 0, 0
        if len(asm_operands) > 0:
            target, target_op_mask = decode_operand(asm_operands[0])
        if len(asm_operands) > 1:
            source, source_op_mask = decode_operand(asm_operands[1])
        opcode_mask = (0x08 | target_op_mask) | (0x00 | source_op_mask)
        masked_machine_opcode = machine_opcode | opcode_mask
        return (masked_machine_opcode, target, source)

    def decode_opcode(self, opcode):
        return OPCODE_MAP[opcode]

    def decode_operand(self, value):
        if value.startswith("@"):
            return REGISTER_MAP[value[1:]], OP_MASK_INDIRECT
        elif value.startswith("#"):
            return int(value[1:], base=16), OP_MASK_DATA
        elif value in REGISTER_MAP.keys():
            return REGISTER_MAP[value], OP_MASK_SIMPLE
        else:
            return int(value, base=16), OP_MASK_SIMPLE
