from config import Day, defaultdict

class Day3(Day):
    def __init__(self, path: str):
        super().__init__(path)
        # complex() for simulating grid positions
        self.vector_map = {
            '>': complex(1, 0),
            '^': complex(0, 1),
            '<': complex(-1, 0),
            'v': complex(0, -1),
        }

    def part1(self):
        houses = defaultdict(int)
        # start at (0,0)
        position = complex()
        for direction in self.content:
            houses[position] += 1
            position += self.vector_map[direction]
        return len(houses)

    def part2(self):
        houses = defaultdict(int)
        santa_pos = robo_pos = complex()
        for direction in self.content:
            houses[santa_pos] += 1
            # change turn on next delivery
            santa_pos, robo_pos = robo_pos, santa_pos
            santa_pos += self.vector_map[direction]
        return len(houses)