from config import np, Day

class Reindeer:
    def __init__(self, speed: int, runtime: int, resttime: int):
        self.speed = speed
        self.runtime = runtime
        self.resttime = resttime

        self.cycle = self.runtime + self.resttime
        self.distance_per_cycle = self.speed * self.runtime

def get_distance(nth_second: int, reindeer: Reindeer):
    time_left = nth_second % reindeer.cycle
    is_running_now = 0 < time_left <= reindeer.runtime
    return reindeer.speed * is_running_now

class Day14(Day):
    def __init__(self, path: str):
        super().__init__(path)

        self.reindeers = [Reindeer(int(tokens[3]), int(tokens[6]), int(tokens[-2]))
                          for line in self.content.splitlines()
                          for tokens in [line.split()]]
        self.n_reindeers = len(self.reindeers)
        self.timespan = 2503

        # for part 2
        self.speeds = np.array([r.speed for r in self.reindeers])
        self.runtimes = np.array([r.runtime for r in self.reindeers])
        resttimes = np.array([r.resttime for r in self.reindeers])
        self.cycles = self.runtimes + resttimes

    def part1(self):
        max_distance = 0
        for reindeer in self.reindeers:
            time_left = self.timespan % reindeer.cycle

            init_distance = reindeer.distance_per_cycle * (self.timespan // reindeer.cycle)
            last_stretch = (reindeer.distance_per_cycle
                            if time_left >= reindeer.runtime
                            else reindeer.speed * time_left)

            max_distance = max(max_distance, init_distance + last_stretch)
        return max_distance

    # original implementation
    def part2_original(self):
        distances = [0] * len(self.reindeers)
        scores = [0] * len(self.reindeers)

        for second in range(1, self.timespan + 1):
            for index in range(self.n_reindeers):
                distances[index] += get_distance(second, self.reindeers[index])
            max_distance = max(distances)
            for index in range(self.n_reindeers):
                scores[index] += distances[index] == max_distance

        return max(scores)

    # rewritten via ChatGPT to use numpy arrays and leverage their vectorizations
    def part2(self):
        # Create a timespan grid for all seconds and reindeers
        timespan = np.arange(1, self.timespan + 1).reshape(-1, 1)  # Shape (timespan, 1)

        # Calculate timespan within the cycle for each reindeer at every second
        time_in_cycle = timespan % self.cycles  # Shape (timespan, n_reindeers)

        # Determine if the reindeer is running at each second
        is_running = (time_in_cycle > 0) & (time_in_cycle <= self.runtimes)  # Boolean array

        # Calculate cumulative distances for each reindeer
        distances = np.cumsum(is_running * self.speeds, axis=0)  # Shape (timespan, n_reindeers)

        # Determine which reindeer is leading at each second
        max_distances = np.max(distances, axis=1, keepdims=True)  # Shape (timespan, 1)
        leaders = distances == max_distances  # Boolean array for leaders

        # Count points for each reindeer
        scores = np.sum(leaders, axis=0)  # Shape (n_reindeers,)

        # Find the maximum score
        return np.max(scores)
