from config import Day, Enum, NamedTuple

Cmd = Enum('Cmd', ['on', 'off', 'toggle'])

class Position(NamedTuple):
    x: int
    y: int

class Instruction(NamedTuple):
    cmd: Cmd
    begin: Position
    end: Position

class Day6(Day):
    def __init__(self, path: str):
        super().__init__(path)
        throwaways = ['turn', 'through']
        cmd_map = {'on': Cmd.on, 'off': Cmd.off, 'toggle': Cmd.toggle}
        self.manual = list()
        for line in self.content.splitlines():
            cmd_str, start_str, end_str = [part for part in line.split(' ')
                                           if part not in throwaways]

            cmd = cmd_map[cmd_str]
            start = Position(*[int(i) for i in start_str.split(',')])
            end   = Position(*[int(i) for i in end_str.split(',')])

            self.manual.append(Instruction(cmd, start, end))

        self.gridlen = 1000
        numlights = self.gridlen ** 2
        self.grid_bool = [False] * numlights
        self.grid_int = [0] * numlights

    def part1(self):
        for instruction in self.manual:
            begin = instruction.begin
            end = instruction.end

            for row in range(begin.x, end.x + 1):
                for col in range(begin.y, end.y + 1):
                    pos = row * self.gridlen + col
                    match instruction.cmd:
                        case Cmd.on:
                            self.grid_bool[pos] = True
                        case Cmd.off:
                            self.grid_bool[pos] = False
                        case Cmd.toggle:
                            self.grid_bool[pos] = not self.grid_bool[pos]

        return self.grid_bool.count(True)

    def part2(self):
        for instruction in self.manual:
            begin = instruction.begin
            end = instruction.end

            for row in range(begin.x, end.x + 1):
                for col in range(begin.y, end.y + 1):
                    pos = row * self.gridlen + col
                    match instruction.cmd:
                        case Cmd.on:
                            self.grid_int[pos] += 1
                        case Cmd.off:
                            self.grid_int[pos] -= self.grid_int[pos] > 0
                        case Cmd.toggle:
                            self.grid_int[pos] += 2

        return sum(self.grid_int)

