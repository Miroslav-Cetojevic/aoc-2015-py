from config import Day, deepcopy

class Day18(Day):
    def __init__(self, path: str):
        super().__init__(path)

        lines = self.content.splitlines()

        # create a "ring" buffer around the actual grid, which allows us to bypass the
        # need to treat first/last rows/columns and all four corners as special cases
        self.n_rows = len(lines) + 2
        self.n_cols = len(lines[0]) + 2
        self.empty_grid = [[0] * self.n_cols for _ in range(self.n_rows)]

        # setting the initial state of the grid
        self.grid = deepcopy(self.empty_grid)
        value_map = {'#': 1, '.': 0}
        for gridrow, strrow in zip(range(1, self.n_rows - 1), range(self.n_rows)):
            for gridcol, strcol in zip(range(1, self.n_cols - 1), range(self.n_cols)):
                self.grid[gridrow][gridcol] = value_map[lines[strrow][strcol]]

        self.steps = 100

        # for part 2: topleft, topright, bottomleft, bottomright
        self.corners = [(1, 1),
                        (1, self.n_cols - 2),
                        (self.n_rows - 2, 1),
                        (self.n_rows - 2, self.n_cols - 2)]

    def part1(self):
        grid = deepcopy(self.grid)
        sums_grid = deepcopy(self.empty_grid)

        for step in range(self.steps):

            for sumsrow, gridrow in zip(sums_grid, grid):
                for col in range(1, self.n_cols - 1):
                    # add lights from the current row
                    sumsrow[col] = gridrow[col - 1] + gridrow[col] + gridrow[col + 1]

            for row in range(1, self.n_rows - 1):
                for col in range(1, self.n_cols - 1):
                    cell = grid[row][col]
                    # add lights from the current column
                    sumlights = (sums_grid[row - 1][col]
                                 + sums_grid[row][col]
                                 + sums_grid[row + 1][col]
                                 - cell)

                    # we are only looking at the current cell in any given iteration,
                    # which means we can overwrite the grid in-place
                    grid[row][col] = int(sumlights == 3 or (sumlights == 2 and cell == 1))

        return sum(row.count(1) for row in grid)

    def turn_on_corners(self, grid: list[list[int]]):
        for row, col in self.corners:
            grid[row][col] = 1

    def part2(self):
        grid = deepcopy(self.grid)
        sums_grid = deepcopy(self.empty_grid)

        self.turn_on_corners(grid)

        for step in range(self.steps):

            for sumsrow, gridrow in zip(sums_grid, grid):
                for col in range(1, self.n_cols - 1):
                    sumsrow[col] = gridrow[col - 1] + gridrow[col] + gridrow[col + 1]

            for row in range(1, self.n_rows - 1):
                for col in range(1, self.n_cols - 1):
                    cell = grid[row][col]
                    sumlights = (sums_grid[row - 1][col]
                                 + sums_grid[row][col]
                                 + sums_grid[row + 1][col]
                                 - cell)
                    grid[row][col] = int(sumlights == 3 or (sumlights == 2 and cell == 1))

            self.turn_on_corners(grid)

        return sum(row.count(1) for row in grid)
