from config import Day, json

def has_red(data: dict):
    for v in data.values():
        if v == 'red':
            return True
    return False

class Day12(Day):
    def __init__(self, path: str):
        super().__init__(path)
        self.json_data = json.loads(self.content)

    def accumulate(self, data):
        result = 0
        datatype = type(data)
        if datatype is dict:
            for e in data: result += self.accumulate(data[e])
        elif datatype is list:
            for e in data: result += self.accumulate(e)
        elif datatype is int:
            result += data
        return result

    def accumulate2(self, data):
        result = 0
        datatype = type(data)
        if datatype is dict and not has_red(data):
            for e in data: result += self.accumulate2(data[e])
        elif datatype is list:
            for e in data: result += self.accumulate2(e)
        elif datatype is int:
            result += data
        return result

    def part1(self):
        return self.accumulate(self.json_data)

    def part2(self):
        return self.accumulate2(self.json_data)
