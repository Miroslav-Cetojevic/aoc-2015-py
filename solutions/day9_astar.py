from config import dataclass, Day, heapify, heappush, heappop, NamedTuple


# conceptually the Visit class represents a bitset akin to C++'s std:bitset
# and emulates its functionality with integer bit manipulation
class Visits:
    def __init__(self):
        self.value = 0

    def set(self, idx: int):
        self.value |= (1 << idx)

    def test(self, idx: int) -> bool:
        return (self.value & (1 << idx)) != 0

    def count(self) -> int:
        return self.value.bit_count()

@dataclass
class State:
    def __init__(self, first: int, last: int, visits: Visits):
        # always make sure the locations (first and last) are sorted, so we can
        # avoid creating equivalent states, thus reducing the search space in half
        # e.g. A->B->C is equivalent to C->B->A.
        self.first, self.last = sorted([first, last])
        self.visits = visits

    def __hash__(self):
        return hash((self.first, self.last, self.visits))

# the priority queue will retrieve the smallest value first, so this
# simple class is used to switch between retrieving the smallest and
# largest value
class Factor(NamedTuple):
    shortest = 1
    longest = -1

class Day9AStar(Day):
    def __init__(self, path: str):
        super().__init__(path)

        self.factor = None
        self.paths = []
        locations = {}
        id_counter = 0
        for line in self.content.splitlines():
            tokens = line.split()
            distance = int(tokens[4])
            loc_ids = []
            for token in (tokens[0], tokens[2]):
                if token not in locations:
                    locations[token] = id_counter
                    self.paths.append([])
                    id_counter += 1
                loc_ids.append(locations[token])
            loc_a, loc_b = loc_ids
            self.paths[loc_a].append((loc_b, distance))
            self.paths[loc_b].append((loc_a, distance))
        self.n_locations = len(locations)
        self.begin_state = State(0, 0, Visits())
        self.begin_state.visits.set(0)
        self.scores = None
        self.queue = None

    # note: any time a heuristic is normally used in this algorithm,
    # it's omitted because for this problem it's treated as zero
    def a_star(self):
        result = 0

        self.scores = {self.begin_state: 0}

        self.queue = []
        heapify(self.queue)
        heappush(self.queue, (0, self.begin_state))

        while self.queue:
            f_score, state = heappop(self.queue)
            g_score = self.scores[state]

            # A* uses the notation f = g + h, where f is a function of the sum of g and h,
            # but since the heuristic is 0 for this solution, h is simply omitted
            if f_score <= g_score:
                if not state.visits.count() == self.n_locations:
                    self.visit_neighbors(state, state.first, state.last)
                    self.visit_neighbors(state, state.last, state.first)
                else:
                    result = g_score
                    break
        return result

    def visit_neighbors(self, state: State, loc_a: int, loc_b: int):
        g_score = self.scores[state]
        for target, distance in self.paths[loc_a]:
            if not state.visits.test(target):
                next_visits = Visits()
                next_visits.value = state.visits.value
                next_visits.set(target)
                next_state = State(target, loc_b, next_visits)
                new_score = g_score + distance
                if next_state not in self.scores or new_score < self.scores[next_state]:
                    # normally the result of the heuristic function would be added to
                    # new_score, but it's zero for this problem, so it's simply omitted
                    self.scores[next_state] = new_score
                    heappush(self.queue, (new_score * self.factor, next_state))

    def part1(self):
        self.factor = Factor.shortest
        return self.a_star()

    def part2(self):
        self.factor = Factor.longest
        return self.a_star()
