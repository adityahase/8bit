import unittest
from emulator import Emulator


class TestEmulator(unittest.TestCase):
    def test_load(self):
        self.emulator = Emulator([1, 0, 0, 0], [["LOAD", "A", "0"]], {"A": 0, "B": 0})
        self.assertEqual(self.emulator.registers["A"], 0)
        state = self.emulator.run()
        next(state)
        self.assertEqual(self.emulator.registers["A"], 1)

    def test_store(self):
        self.emulator = Emulator([0, 0, 0, 0], [["STORE", "0", "A"]], {"A": 1, "B": 0})
        self.assertEqual(self.emulator.memory[0], 0)
        state = self.emulator.run()
        next(state)
        self.assertEqual(self.emulator.memory[0], 1)

    def test_add(self):
        self.emulator = Emulator([0, 0, 0, 0], [["ADD", "A", "B"]], {"A": 1, "B": 1})
        self.assertEqual(self.emulator.registers["A"], 1)
        state = self.emulator.run()
        next(state)
        self.assertEqual(self.emulator.registers["A"], 2)

    def test_multiple_instruction(self):
        self.emulator = Emulator(
            [1, 1, 0, 0],
            [
                ["LOAD", "A", "0"],
                ["LOAD", "B", "1"],
                ["ADD", "A", "B"],
                ["STORE", "2", "A"]
            ],
            {"A": 0, "B": 0}
        )
        state = self.emulator.run()

        self.assertEqual(self.emulator.registers["A"], 0)

        next(state)
        self.assertEqual(self.emulator.registers["A"], 1)
        self.assertEqual(self.emulator.registers["B"], 0)

        next(state)
        self.assertEqual(self.emulator.registers["B"], 1)

        next(state)
        self.assertEqual(self.emulator.registers["A"], 2)
        self.assertEqual(self.emulator.registers["B"], 1)
        self.assertEqual(self.emulator.memory[2], 0)

        next(state)
        self.assertEqual(self.emulator.memory[2], 2)

if __name__ == '__main__':
    unittest.main()
