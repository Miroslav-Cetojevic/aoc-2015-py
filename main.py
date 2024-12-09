from config import join, NamedTuple, Number, perf_counter_ns
from solutions.day1 import Day1
from solutions.day14 import Day14
from solutions.day2 import Day2
from solutions.day3 import Day3
from solutions.day4 import Day4
from solutions.day5 import Day5
from solutions.day6 import Day6
from solutions.day7 import Day7
from solutions.day8 import Day8
from solutions.day9 import Day9
from solutions.day9_astar import Day9AStar
from solutions.day9_astar2 import Day9AStar2
from solutions.day10 import Day10
from solutions.day11 import Day11
from solutions.day12 import Day12
from solutions.day13 import Day13


class Result(NamedTuple):
    value: Number
    milliseconds: float

def avg_runtime(func, n):
    start = perf_counter_ns()
    for _ in range(n):
        value = func()
    end = perf_counter_ns()
    milliseconds = ((end - start) / n) / 1_000_000
    return Result(value, milliseconds)

if __name__ == '__main__':
    day9 = {'brute': Day9, 'astar': Day9AStar, 'astar2': Day9AStar2}
    day14 = {'list': Day14, 'numpy': Day14Numpy}
    all_days = [Day1, Day2, Day3, Day4, Day5, Day6, Day7, Day8, day9['brute'], Day10,
                Day11, Day12, Day13, day14['list']]
    journal = {i: func for i, func in enumerate(all_days, start=1)}

    index = 14
    chosen_day = journal[index](join('inputs', f'day{index}-input'))
    print('Part 1:', avg_runtime(chosen_day.part1, 1_000_000))
    print('Part 2:', avg_runtime(chosen_day.part2, 10_000))

