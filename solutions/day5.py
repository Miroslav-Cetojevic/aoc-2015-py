from config import Day, pairwise

class Day5(Day):
    def __init__(self, path: str):
        super().__init__(path)
        self.strings = self.content.splitlines()
        self.bad_pairs = (('a', 'b'), ('c', 'd'), ('p', 'q'), ('x', 'y'))
        self.vowels = 'aeiou'

    def part1(self):
        return sum(
            not any(pair in self.bad_pairs for pair in pairwise(string)) # no bad pair
            and any(l1 == l2 for l1, l2 in pairwise(string)) # twin letters
            and sum(char in self.vowels for char in string) >= 3 # triple vowels
            for string in self.strings
        )

    def part2(self):
        return sum(
            any(f'{string[i-1]}{string[i]}' in string[i+1:] for i in range(1, len(string))) # repeat pairs
            and any(string[i] == string[i-2] for i in range(2, len(string))) # letter sandwich
            for string in self.strings
        )
