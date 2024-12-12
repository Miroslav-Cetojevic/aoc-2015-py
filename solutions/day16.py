from config import Day, re

class Day16(Day):
    def __init__(self, path: str):
        super().__init__(path)

        self.my_aunt = {'children': 3, 'cats': 7, 'samoyeds': 2, 'pomeranians': 3, 'akitas': 0,
                        'vizslas': 0, 'goldfish': 5, 'trees': 3, 'cars': 2, 'perfumes': 1}
        # \w+ for matching lowercase words, colons and numbers
        pattern = re.compile(r'(\w+): (\d+)')
        self.aunts = [{key: int(value) for key, value in pattern.findall(line)}
                      for line in self.content.splitlines()]

        # for part 2
        self.higher_valued = ['cats', 'trees']
        self.lower_valued = ['pomeranians', 'goldfish']

    def part1(self):
        for aunt_id, clues in enumerate(self.aunts, start=1):
            has_all = True
            for clue, num in clues.items():
                if self.my_aunt[clue] != num:
                    has_all = False
                    break
            if has_all:
                return aunt_id
        return None

    def part2(self):
        for aunt_id, clues in enumerate(self.aunts, start=1):
            has_all = True
            for clue, num in clues.items():
                my_num = self.my_aunt[clue]
                if clue in self.higher_valued:
                    result = num > my_num
                elif clue in self.lower_valued:
                    result = num < my_num
                else:
                    result = num == my_num
                if not result:
                    has_all = False
                    break
            if has_all:
                return aunt_id
        return None
