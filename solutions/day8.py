from config import Day

class Day8(Day):
    def __init__(self, path: str):
        super().__init__(path)
        self.backslash = '\\'
        self.content_len = len(self.content)

    def part1(self):
        escsum = 0
        escmemsum = 0
        nlsum = 0

        content_iter = iter(self.content)
        for char in content_iter:
            if char == self.backslash:
                char = next(content_iter)
                escmemsum += 1
                if char == self.backslash or char == '\"':
                    escsum += 2
                else:
                    escsum += 4
                    next(content_iter)
                    next(content_iter)
            elif char == '\n':
                nlsum += 1

        # codesum = self.content_len - nlsum
        # memsum = codesum - (nlsum * 2) - escsum + escmemsum
        # result = codesum - memsum

        # return value has been simplified from the commented-out code above
        return nlsum * 2 + escsum - escmemsum

    def part2(self):
        encsum = 0
        nlsum = 0

        content_iter = iter(self.content)
        for char in content_iter:
            if char == self.backslash:
                char = next(content_iter)
                if char == self.backslash or char == '\"':
                    encsum += 2
                else:
                    encsum += 1
                    next(content_iter)
                    next(content_iter)
            elif char == '\n':
                nlsum += 1

        # codesum = self.content_len - nlsum
        # encodesum = codesum + (4 * nlsum) + encsum
        # result = encodesum - codesum

        # return value has been simplified from the commented-out code above
        return nlsum * 4 + encsum
