from config import Day, permutations, pairwise, sys

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
