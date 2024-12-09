from config import dataclass, heappop, heappush, heapreplace, math, NamedTuple, operator
from solutions.day import Day


class AdjacencyMatrix(list):
    def __init__(self):
        super().__init__()

    def lookup(self, x, y):
        triangle = lambda n: (n * (n - 1)) // 2
        min_id, max_id = sorted((x, y))
        return self.__getitem__(triangle(max_id) + min_id)

@dataclass
class State:
    def __init__(self, first: int = 0, last: int = 0, visits: int = 1):
        # always make sure the locations (first and last) are sorted, so we can
        # avoid creating equivalent states, thus reducing the search space in half
        # e.g. A->B->C is equivalent to C->B->A.
        self.first, self.last = sorted((first, last))
        self.visits = visits

    def __hash__(self):
        return hash((self.first, self.last, self.visits))

# concept adapted from https://stackoverflow.com/a/33181173
class Heap:
    def __init__(self, max_size, cmp):
        self.max_size = max_size
        self.cmp = cmp
        self.data = []

    def insert(self, value):
        if len(self.data) < self.max_size:
            heappush(self.data, value)
        elif self.cmp(value, self.data[0]):
            heapreplace(self.data, value)

# this simple class will let me change the behavior of the heap and priority queue,
# a comparator for heap and a factor for the queue to get the desired ordering
class Output(NamedTuple):
    min_value = operator.lt, 1
    max_value = operator.gt, -1

class Day9AStar2(Day):
    def __init__(self, filepath: str):
        super().__init__(filepath)

        self.paths = AdjacencyMatrix()

        for line in self.content.splitlines():
            last_token = line.split()[-1]
            distance = int(last_token)
            self.paths.append(distance)

        # Conceptually, the matrix looks like this:
        #   (1,0)
        #   (2,0), (2,1)
        #   (3,0), (3,1), (3,2)
        # The ordering is:
        #   (1,0), (2,0), (2,1), (3,0), (3,1), (3,2)
        #
        # However, in the input the distances are grouped by point of origin,
        # and the next group has alway one entry less to avoid the duplicate
        # entry from the previous group (remember: A->B is equal to B->A).
        #
        # So we end up with an ordering that would translate to:
        #   (3,2) (3,1) (3,0)
        #   (2,1) (2,0)
        #   (1,0)
        # which won't work for an adjacency matrix. So we reverse the list.
        self.paths.reverse()

        triangle_root = lambda x: int((math.sqrt(8 * (x + 1)) - 1) // 2)
        self.n_locations = triangle_root(len(self.paths)) + 1

        self.begin_state = State()
        self.queue = None
        self.scores = None
        self.cmp = None
        self.factor = None
        self.goal_not_reached = lambda state: state.visits.bit_count() < self.n_locations
        self.not_visited = lambda state, loc_id: (state.visits & (1 << loc_id)) == 0

    def for_each_neighbor(self, state: State, g_score: int):
        for loc_id in range(self.n_locations):
            if self.not_visited(state, loc_id):
                new_visits = state.visits | (1 << loc_id)
                args = (state.first, loc_id), (loc_id, state.last), (state.last, state.first)
                for first, last, lookup_id in zip(*args):
                    next_state = State(first, last, new_visits)
                    distance = self.paths.lookup(lookup_id, loc_id)
                    new_score = g_score + distance
                    if next_state not in self.scores or new_score < self.scores[next_state]:
                        self.scores[next_state] = new_score
                        priority = (new_score + self.heuristic(next_state)) * self.factor
                        heappush(self.queue, (priority, next_state))

    # estimate lowest cost from the current location to the goal
    def heuristic(self, state: State):
        result = 0
        visits = state.visits
        num_visits = visits.bit_count()
        if num_visits < self.n_locations:
            max_size = self.n_locations - num_visits - 1
            values = Heap(max_size, self.cmp)
            # every state has visited the 0th location, since they have to start somewhere
            for first in range(1, self.n_locations):
                if self.not_visited(state, first):
                    for last in range(first):
                        if self.not_visited(state, last):
                            values.insert(self.paths.lookup(first, last))
            result = sum(values.data)
        return result

    def a_star(self):
        start = self.begin_state

        result = 0
        self.queue = [(self.heuristic(start), start)]
        self.scores = {start: 0}

        while self.queue:
            f_score, state = heappop(self.queue)
            g_score = self.scores[state]

            if f_score - self.heuristic(state) <= g_score:
                if self.goal_not_reached(state):
                    self.for_each_neighbor(state, g_score)
                else:
                    result = g_score
                    break
        return result

    def part1(self):
        self.cmp, self.factor = Output.min_value
        return self.a_star()

    def part2(self):
        self.cmp, self.factor = Output.max_value
        return self.a_star()
