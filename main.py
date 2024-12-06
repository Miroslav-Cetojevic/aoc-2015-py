from config import *
from solutions.day1 import Day1
from solutions.day2 import Day2
from solutions.day3 import Day3
from solutions.day4 import Day4
from solutions.day5 import Day5
from solutions.day6 import Day6
from solutions.day7 import Day7
from solutions.day8 import Day8
from solutions.day9 import Day9


class Result(NamedTuple):
    value: Number
    milliseconds: float

def avg_runtime(func, n):
    value = func()
    start = perf_counter_ns()
    for _ in range(n):
        func()
    end = perf_counter_ns()
    milliseconds = ((end - start) / n) / 1_000_000
    return Result(value, milliseconds)

if __name__ == '__main__':
    all_days = [Day1, Day2, Day3, Day4, Day5, Day6, Day7, Day8, Day9]
    journal = {i: func for i, func in enumerate(all_days, start=1)}

    index = 9
    chosen_day = journal[index](join('inputs', f'day{index}-input'))
    print('Part 1:', avg_runtime(chosen_day.part1, 100))
    print('Part 2:', avg_runtime(chosen_day.part2, 100))

