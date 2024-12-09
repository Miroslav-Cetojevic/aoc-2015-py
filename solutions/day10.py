from solutions.day import Day


class Day10(Day):
    def __init__(self, path: str):
        super().__init__(path)
        self.puzzle = [int(digit) for digit in self.content.strip()]

    def look_and_say(self, cycles: int):
        result = self.puzzle
        for _ in range(cycles):
            tmp = []
            index = 0
            while index < len(result):
                digit = result[index]
                count = 1
                while index + count < len(result) and result[index + count] == digit:
                    count += 1
                tmp.append(count)
                tmp.append(digit)
                index += count
            result = tmp
        return len(result)

    def part1(self):
        return self.look_and_say(cycles=40)

    def part2(self):
        return self.look_and_say(cycles=50)

