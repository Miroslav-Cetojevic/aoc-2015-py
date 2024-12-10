from collections import defaultdict, UserList
from copy import deepcopy, copy
from functools import singledispatchmethod, singledispatch
from itertools import pairwise
from operator import itemgetter

from config import Day, pprint
from support import next_permutation

def triangle(n: int):
    return (n * (n - 1)) // 2

def index(pair: list):
    pair.sort()
    col, row = pair
    return triangle(row) + col

# implement an adjacency matrix to replace the dictionary in v1
class Happymeter(UserList):
    def __init__(self, size: int):
        super().__init__([0] * triangle(size))

    def __getitem__(self, pair):
        return super().__getitem__(index(pair))

    def __setitem__(self, pair, value):
        super().__setitem__(index(pair), value)

class Day13V2(Day):
    def __init__(self, path: str):
        super().__init__(path)

        people_map = {}
        person_id = 0

        self.people = set()
        attitude = {'gain': 1, 'lose': -1}
        self.scores = {}

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

        self.happymeter = Happymeter(len(self.people))
        me = len(self.people)
        self.people_plus = copy(self.people)
        self.people_plus.add(me)
        self.happymeter_plus = Happymeter(len(self.people_plus))
        for pair_ids, happiness in self.scores.items():
            pair_as_list = list(pair_ids)
            self.happymeter[pair_as_list] += happiness
            self.happymeter_plus[pair_as_list] += happiness
            for person_id in pair_ids:
                self.happymeter_plus[[person_id, me]] = 0

        self.seating = lambda s: [0] * len(s)

    def get_happiness(self, seating, happymeter):
        begin = 0
        end = len(seating) - 1

        first = seating[0]
        last = seating[-1]
        next_to_last = seating[-2]

        penultimate_score = happymeter[[first, next_to_last]]
        total_score = min_score = penultimate_score

        for a, b in pairwise(seating[begin:end]):
            score = happymeter[[a, b]]
            total_score += score
            min_score = min(min_score, score)

        total_score -= min_score
        total_score += happymeter[[next_to_last, last]]
        total_score += happymeter[[first, last]]
        return total_score

    def find_max_happiness(self, include_me: bool = False):
        max_happiness = 0

        happymeter = self.happymeter_plus if include_me else self.happymeter
        seating = self.seating(self.people_plus) if include_me else self.seating(self.people)
        n_people = len(seating)
        n_permutable_seats = n_people - 1
        range_stop = n_permutable_seats - 1
        seating[1] = 0
        seating[-1] = n_permutable_seats
        for i in range(1, range_stop):
            seating[0] = i
            for j in range(i + 1, n_permutable_seats):
                seating[2] = j
                current = 0
                for k in range(3, n_permutable_seats):
                    current += 1
                    while current == i or current == j:
                        current += 1
                    seating[k] = current
                while True:
                    max_happiness = max(max_happiness, self.get_happiness(seating, happymeter))
                    if not next_permutation(seating):
                        break

        # filtered = set()
        # while len(filtered) < n_people:
        #     first, last = seating[0], seating[-1]
        #     if first not in filtered:
        #         filtered.add(first)
        #     if last not in filtered:
        #         total_happiness = happymeter[[first, last]]
        #         for p1, p2 in pairwise(seating):
        #             total_happiness += happymeter[[p1, p2]]
        #         max_happiness = max(max_happiness, total_happiness)
        #     if not next_permutation(seating):
        #         break
        return max_happiness

    def part1(self):
        return self.find_max_happiness()

    def part2(self):
        pass
        # return self.find_max_happiness(include_me=True)
