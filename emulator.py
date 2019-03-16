class Emulator(object):
    def __init__(self, memory, program, registers):
        self.memory = memory
        self.program = program
        self.registers = registers

    def run(self):
        for instruction in self.program:
            opcode, operand1, operand2 = instruction
            if opcode == "LOAD":
                self.registers[operand1] = self.memory[int(operand2)]
            elif opcode == "STORE":
                self.memory[int(operand1)] = self.registers[operand2]
            elif opcode == "ADD":
                self.registers[operand1] += self.registers[operand2]
            yield self.state()

    def state(self):
        return {
            "memory": self.memory,
            "registers": self.registers
        }
