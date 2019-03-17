import unittest
from emulator import Emulator


class TestEmulator(unittest.TestCase):
    def test_move_memory(self):
        self.emulator = Emulator(program=[["MOV", "A", "80"]])
        self.emulator.memory[80] = 100
        self.assertEqual(self.emulator.registers()["A"], 0)
        state = self.emulator.run()
        next(state)
        self.assertEqual(self.emulator.registers()["A"], 100)

    def test_add(self):
        self.emulator = Emulator(program=[["MOV", "A", "80"], ["MOV", "B", "81"], ["ADD", "A", "B"]])
        self.emulator.memory[0x80] = 10
        self.emulator.memory[0x81] = 20
        state = self.emulator.run()
        self.assertEqual(self.emulator.registers()["A"], 0)
        next(state)
        self.assertEqual(self.emulator.registers()["A"], 10)
        self.assertEqual(self.emulator.registers()["B"], 0)
        next(state)
        self.assertEqual(self.emulator.registers()["B"], 20)
        next(state)
        self.assertEqual(self.emulator.registers()["A"], 30)

    def test_jmp(self):
        self.emulator = Emulator(program=[
            ["MOV", "A", "80"],
            ["MOV", "B", "81"],
            ["SUB", "A", "B"],
            ["NOP", "6", "6"],
            ["JNZ", "A", "0A"],
            ["HLT"]
        ])
        state = self.emulator.run()
        self.emulator.memory[0x80] = 20
        self.emulator.memory[0x81] = 10

        self.assertEqual(self.emulator.registers()["A"], 0)
        next(state)
        self.assertEqual(self.emulator.registers()["A"], 20)
        self.assertEqual(self.emulator.registers()["B"], 0)

        next(state)
        self.assertEqual(self.emulator.registers()["B"], 10)

        next(state)
        self.assertEqual(self.emulator.registers()["A"], 10)
        self.assertEqual(self.emulator.registers()["B"], 10)
        self.assertEqual(self.emulator.registers()["PC"], 9)

        next(state)
        next(state)
        next(state)
        next(state)
        self.assertEqual(self.emulator.registers()["PC"], 6)

        next(state)
        next(state)
        next(state)
        print(self.emulator.state())
        self.assertEqual(self.emulator.registers()["A"], 0)
        self.assertEqual(self.emulator.registers()["PC"], C)

        next(state)
        self.assertEqual(self.emulator.registers()["PC"], C)

if __name__ == '__main__':
    unittest.main()
