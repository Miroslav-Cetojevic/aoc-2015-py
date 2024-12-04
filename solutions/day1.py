from config import Day, np

class Day1(Day):
    def __init__(self, path: str):
        super().__init__(path)
        input_map = {'(': 1, ')': -1, '\n': 0}
        self.instructions = np.fromiter([input_map[char] for char in self.content], dtype=int)

    def part1(self):
        return np.sum(self.instructions)

    def part2(self):
        floor = 0
        position = 0
        for index, step in enumerate(self.instructions, start=1):
            floor += step
            if floor == -1:
                position = index
                break
        return position
