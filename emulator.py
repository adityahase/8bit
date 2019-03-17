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

REVERSE_OPCODE_MAP = {
    0x00: "NOP",
    0x10: "ADD",
    0x20: "AND",
    0x30: "DEC",
    0x40: "DIV",
    0x50: "INC",
    0x60: "JMP",
    0x70: "JZ",
    0x80: "MOV",
    0x90: "MUL",
    0xA0: "NEG",
    0xB0: "SUB",
    0xC0: "OR",
    0xD0: "XOR",
    0xF0: "HLT"
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

MEMORY_SIZE = 256

class Emulator(object):
    def __init__(self, memory=None, program=None, registers=None):
        self.memory = [0]*MEMORY_SIZE
        self.code = []
        for instruction in Assembler(program).assemble():
            self.code.extend(instruction)
        for index, instruction in enumerate(self.code):
            self.memory[index] = instruction

    def registers(self):
        return {key: self.memory[value] for key, value in REGISTER_MAP.items()}

    def run(self):
        program_counter = REGISTER_MAP["PC"]
        print(self.state())
        while True:
            pointer = self.memory[program_counter]
            instruction = self.memory[pointer: pointer + 3]
            opcode, target, source, target_mask, source_mask = self.decode(instruction)
            function = {
                "NOP": self.OP_NOP,
                "ADD": self.OP_ADD,
                "AND": self.OP_AND,
                "DEC": self.OP_DEC,
                "DIV": self.OP_DIV,
                "INC": self.OP_INC,
                "JMP": self.OP_JMP,
                "JZ": self.OP_JZ,
                "MOV": self.OP_MOV,
                "MUL": self.OP_MUL,
                "NEG": self.OP_NEG,
                "SUB": self.OP_SUB,
                "OR": self.OP_OR,
                "XOR": self.OP_XOR,
                "HLT": self.OP_HLT
            }[REVERSE_OPCODE_MAP[opcode]]
            function(self.resolve(target, target_mask), self.resolve(source, source_mask))
            self.memory[program_counter] += 3
            yield self.state()

    def OP_NOP(self, target, source):
        pass


    def resolve(self, value, mask):
        return {
            OP_MASK_SIMPLE: value,
            OP_MASK_INDIRECT: self.memory[value]
        }[mask]

    def decode(self, instruction):
        opcode, target, source = instruction
        unmasked_opcode = opcode & 0xF0
        opcode_mask = opcode & 0x0F
        target_op_mask = opcode_mask & 0x0C >> 2
        source_op_mask = opcode_mask & 0x03
        return unmasked_opcode, target, source, target_op_mask, source_op_mask


    def state(self):
        return {
            "memory": self.memory,
            "registers": self.registers()
        }


class Assembler(object):
    def __init__(self, program):
        self.program = program

    def assemble(self):
        return [self.encode(instruction) for instruction in self.program]

    def encode(self, asm_instruction):
        asm_opcode, *asm_operands = asm_instruction
        machine_opcode = self.encode_opcode(asm_opcode)
        target, source = 0, 0
        if len(asm_operands) > 0:
            target, target_op_mask = self.encode_operand(asm_operands[0])
        if len(asm_operands) > 1:
            source, source_op_mask = self.encode_operand(asm_operands[1])
        opcode_mask = (target_op_mask << 2) | source_op_mask
        masked_machine_opcode = machine_opcode | opcode_mask
        return (masked_machine_opcode, target, source)

    def encode_opcode(self, opcode):
        return OPCODE_MAP[opcode]

    def encode_operand(self, value):
        if value.startswith("@"):
            return REGISTER_MAP[value[1:]], OP_MASK_INDIRECT
        elif value in REGISTER_MAP.keys():
            return REGISTER_MAP[value], OP_MASK_SIMPLE
        else:
            return int(value, base=16), OP_MASK_SIMPLE
