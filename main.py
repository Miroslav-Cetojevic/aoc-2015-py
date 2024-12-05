from config import *
from solutions.day1 import Day1
from solutions.day2 import Day2
from solutions.day3 import Day3
from solutions.day4 import Day4
from solutions.day5 import Day5


class Result(NamedTuple):
    value: Number
    milliseconds: float

def avg_runtime(func, n):
    value = func()
    start = perf_counter_ns()
    for _ in range(n):
        func()
    end = perf_counter_ns()
    return Result(value, ((end - start) / n) / 1_000_000)

if __name__ == '__main__':
    all_days = [Day1, Day2, Day3, Day4, Day5]
    journal = {i: func for i, func in enumerate(all_days, start=1)}

    index = 5
    chosen_day = journal[index](join('inputs', f'day{index}-input'))
    print('Part 1:', avg_runtime(chosen_day.part1, 1_000))
    print('Part 2:', avg_runtime(chosen_day.part2, 1_000))

