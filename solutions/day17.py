from config import Day, defaultdict, Enum

SolveType = Enum('SolveType', ['Recursion', 'DynamicProgramming', 'Memoization'])
Part = Enum('Part', ['One', 'Two'])

class Day17(Day):
    def __init__(self, path: str):
        super().__init__(path)
        self.containers = [int(size) for size in self.content.splitlines()]
        self.n_containers = len(self.containers)
        self.target_volume = 150
        self.solutions = {
            SolveType.Recursion: {
                Part.One: self.get_n_combos_rec,
                Part.Two: self.get_min_combos_rec
            },
            SolveType.DynamicProgramming: {
                Part.One: self.get_n_combos_dp,
                Part.Two: self.get_min_combos_dp
            },
            SolveType.Memoization: {
                Part.One: self.get_n_combos_memo,
                Part.Two: self.get_min_combos_memo
            }
        }

    def get_n_combos_rec(self, target_volume: int = None, containers: list[int] = None):
        if target_volume is None:
            target_volume = self.target_volume
        if containers is None:
            containers = self.containers

        if target_volume == 0:
            return 1
        n_combos = 0
        for i in range(len(containers)):
            volume = containers[i]
            remaining_volume = target_volume - volume
            if remaining_volume >= 0:
                n_combos += self.get_n_combos_rec(remaining_volume, containers[i + 1:])
        return n_combos

    def get_n_combos_dp(self):
        kitchen = [0] * (self.target_volume + 1)
        kitchen[0] = 1
        for c in self.containers:
            for v in range(self.target_volume, c - 1, -1):
                kitchen[v] += kitchen[v - c]
        return kitchen[self.target_volume]

    def get_n_combos_memo(self, target_volume: int = None, containers: list[int] = None):
        if target_volume is None:
            target_volume = self.target_volume
        if containers is None:
            containers = self.containers

        memo = {}

        def memoize(target, index):
            if target == 0:
                return 1
            if target < 0 or index == len(containers):
                return 0
            if (target, index) in memo:
                return memo[(target, index)]

            # Either use the current container or skip it
            memo[(target, index)] = memoize(target - containers[index], index + 1) + memoize(target, index + 1)
            return memo[(target, index)]

        return memoize(target_volume, 0)

    def part1(self):
        # dynamic programming is the fastest variant for this part
        return self.solutions[SolveType.DynamicProgramming][Part.One]()

    def get_min_combos_rec(self):
        def get_combos(target_volume: int, containers: list[int]):
            if target_volume == 0:
                return [[]]
            combos = []
            for i in range(len(containers)):
                volume = containers[i]
                remaining_volume = target_volume - volume
                if remaining_volume >= 0:
                    remaining_combos = get_combos(remaining_volume, containers[i + 1:])
                    for remaining_combo in remaining_combos:
                        combos.append([volume] + remaining_combo)
            return combos

        result = defaultdict(int)
        min_num = self.n_containers
        for combo in get_combos(self.target_volume, self.containers):
            tmp_num = len(combo)
            result[tmp_num] += 1
            min_num = min(min_num, tmp_num)
        return result[min_num]

    def get_min_combos_dp(self):
        kitchen = [[0] * (self.n_containers + 1) for i in range(self.target_volume + 1)]
        kitchen[0][0] = 1
        for c in self.containers:
            for v in range(self.target_volume - c, -1, -1):
                for n in range(self.n_containers, 0, -1):
                    kitchen[v + c][n] += kitchen[v][n - 1]
        fridge = kitchen[self.target_volume]
        return next(num_combos for num_combos in fridge if num_combos > 0)

    def get_min_combos_memo(self):

        def get_combos(target_volume: int = None, containers: list[int] = None):
            if target_volume is None:
                target_volume = self.target_volume
            if containers is None:
                containers = self.containers

            memo = {}

            def memoize(target, index):
                if target == 0:
                    return [[]]
                if target < 0 or index == len(containers):
                    return []
                if (target, index) in memo:
                    return memo[(target, index)]

                # Include or exclude the current container
                include = [[containers[index]] + combo
                           for combo in memoize(target - containers[index], index + 1)]
                exclude = memoize(target, index + 1)
                memo[(target, index)] = include + exclude
                return memo[(target, index)]

            return memoize(target_volume, 0)

        combos = get_combos()
        min_size = min(len(combo) for combo in combos)
        return sum(len(combo) == min_size for combo in combos)

    def part2(self):
        # dynamic programming is the fastest variant for this part, too
        return self.solutions[SolveType.DynamicProgramming][Part.Two]()