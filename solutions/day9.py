from config import Day, deepcopy, next_permutation, pairwise, sys

def permutations(sequence: list):
    result = list()

    if not sequence or len(sequence) == 1:
        result.append(sequence)
    else:
        sequence.sort()
        filtered = set()

        # given a sorted list, a completed set of permutations with the same first element
        # means that any subsequent permutation with that element in the last position is
        # a mirror to one of the existing permutations, i.e. same path, same distance.
        # We skip these by updating our filter with each new element that appears first in
        # a permutation. Once all elements of a permutation are in the filter, we are done.
        while len(filtered) < len(sequence):
            first = sequence[0]
            last = sequence[-1]
            if first not in filtered:
                filtered.add(first)
            if last not in filtered:
                result.append(deepcopy(sequence))
            if not next_permutation(sequence):
                break

    return result

class Day9(Day):
    def __init__(self, path: str):
        super().__init__(path)
        self.places = set()
        self.paths = dict()

        for line in self.content.splitlines():
            tokens = line.split()
            locations = (tokens[0], tokens[2])
            self.places.update(locations)
            self.paths[frozenset(locations)] = int(tokens[-1])

        self.adjacency_matrix = list()
        for loc_id, origin in enumerate(self.places):
            self.adjacency_matrix.append([])
            for destination in self.places:
                # print(origin, destination)
                connection = frozenset((origin, destination))
                distance = 0 if connection not in self.paths else self.paths[connection]
                self.adjacency_matrix[loc_id].append(distance)

    def part1(self):
        shortest_path = sys.maxsize
        places = list(self.places)
        for path in permutations(places):
            total_distance = 0
            for a, b in pairwise(path):
                total_distance += self.paths[frozenset([a, b])]
            if total_distance < shortest_path:
                shortest_path = total_distance
        # note: I tried using sum() and min() in place of the loop and
        # conditional and I found that they made the program slightly slower
        return shortest_path

    def part2(self):
        longest_path = 0
        places = list(self.places)
        for path in permutations(places):
            total_distance = 0
            for a, b in pairwise(path):
                total_distance += self.paths[frozenset([a, b])]
            if total_distance > longest_path:
                longest_path = total_distance
        return longest_path
