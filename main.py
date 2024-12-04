from config import *
from solutions.day1 import Day1
from solutions.day2 import Day2


class Result(NamedTuple):
    value: Any
    milliseconds: float

def avg_runtime(func, n):
    value = func()
    start = perf_counter_ns()
    for _ in range(n):
        func()
    end = perf_counter_ns()
    return Result(value, ((end - start) / n) / 1_000_000)

if __name__ == '__main__':
    all_days = {i: func for i, func in enumerate([Day1, Day2], start=1)}

    index = 2
    chosen_day = all_days[index](join('inputs', f'day{index}-input'))
    print('Part 1:', avg_runtime(chosen_day.part1, 10_000))
    print('Part 2:', avg_runtime(chosen_day.part2, 10_000))

