from config import join, NamedTuple, Number, perf_counter_ns
from solutions.day1 import Day1
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
from solutions.day14 import Day14
from solutions.day15 import Day15
from solutions.day16 import Day16
from solutions.day17 import Day17
from solutions.day18 import Day18
from solutions.day19 import Day19
from solutions.day20 import Day20
from solutions.day21 import Day21
from solutions.day21_v2 import Day21v2


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
    # Day 9 notes: the first A* algorithm implementation uses the concept of C++'s std::bitset
    # to store the visited locations and seems to be the fastest solution for part 2 (max distance).
    # The second A* algorithm implementation uses dedicated adjacency matrix and a specialized heap,
    # which seems to be the fastest solution for part 1 (min distance)
    day9 = {'brute': Day9, 'astar': Day9AStar, 'astar2': Day9AStar2}
    day21 = {'v1': Day21, 'v2': Day21v2}
    all_days = [Day1, Day2, Day3, Day4, Day5, Day6, Day7, Day8, day9['astar2'], Day10,
                Day11, Day12, Day13, Day14, Day15, Day16, Day17, Day18, Day19, Day20,
                day21['v2'],]
    journal = {i: func for i, func in enumerate(all_days, start=1)}

    index = len(all_days)
    # index = 9
    chosen_day = journal[index](join('inputs', f'day{index}-input'))
    print('Part 1:', avg_runtime(chosen_day.part1, 100_000))
    print('Part 2:', avg_runtime(chosen_day.part2, 100_000))

