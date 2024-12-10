from config import copy, Day, defaultdict, itemgetter, pairwise
from support import next_permutation

class Day13(Day):
    def __init__(self, path: str):
        super().__init__(path)
        # intermediate data
        people_map = {}
        person_id = 0

        self.people = set()
        self.scores = {}
        attitude = {'gain': 1, 'lose': -1}

        for line in self.content.splitlines():
            tokens = line.strip('.').split()
            pair = (tokens[0], tokens[-1])
            for person in pair:
                if person not in people_map:
                    people_map[person] = person_id
                    person_id += 1
            pair_ids = itemgetter(*pair)(people_map)
            self.people.update(pair_ids)
            score = int(tokens[3])
            modifier = attitude[tokens[2]]
            self.scores[pair_ids] = score * modifier

        # frozenset((a, b)) is equal to frozenset((b, a)), which allows me to add
        # their values to the same key
        self.happymeter = defaultdict(int)
        for pair_ids, happiness in self.scores.items():
            self.happymeter[frozenset(pair_ids)] += happiness

        # for part 2
        self.happymeter_plus = copy(self.happymeter)
        me = len(self.people)
        for person in self.people:
            pair = (person, me)
            self.happymeter_plus[frozenset(pair)] = 0
        self.people_plus = copy(self.people)
        self.people_plus.add(me)

    def find_max_happiness(self, include_me: bool = False):
        happymeter = self.happymeter_plus if include_me else self.happymeter
        seating = list(self.people_plus) if include_me else list(self.people)
        max_happiness = 0
        filtered = set()

        n_people = len(seating)

        while len(filtered) < n_people:
            first, last = seating[0], seating[-1]
            if first not in filtered:
                filtered.add(first)
            if last not in filtered:
                total_happiness = happymeter[frozenset((first, last))]
                for pair in pairwise(seating):
                    total_happiness += happymeter[frozenset(pair)]
                max_happiness = max(max_happiness, total_happiness)
            # this function already takes equivalent permutations into account
            if not next_permutation(seating):
                break
        return max_happiness

    def part1(self):
        return self.find_max_happiness()

    def part2(self):
        return self.find_max_happiness(include_me=True)
