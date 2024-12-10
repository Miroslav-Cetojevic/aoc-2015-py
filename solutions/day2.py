from config import Day

class Day2(Day):
    def __init__(self, path: str):
        super().__init__(path)
        self.paper_order = [[int(i) for i in line.split('x')]
                            for line in self.content.splitlines()]

    def part1(self):
        total_paper = 0
        for dimensions in self.paper_order:
            dimensions.sort()
            a, b, c = dimensions
            areas = [a * b, a * c, b * c]
            # since the dimensions are sorted at the start, the first
            # calculated area is guaranteed to be the smallest in the list
            total_paper += 2 * sum(areas) + areas[0]
        return total_paper

    def part2(self):
        total_ribbon = 0
        for dimensions in self.paper_order:
            dimensions.sort()
            a, b, c = dimensions
            total_ribbon += (2 * (a + b)) + (a * b * c)
        return total_ribbon
