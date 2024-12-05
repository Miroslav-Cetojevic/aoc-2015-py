from config import Day, hashlib, itertools

class Day4(Day):
    def __init__(self, path: str):
        super().__init__(path)
        self.strkey = self.content.strip()

    def part1(self):
        result = 0
        for numkey in itertools.count(start=1):
            md5_input = f'{self.strkey}{str(numkey)}'
            md5_hash = hashlib.md5(md5_input.encode())
            digest = md5_hash.digest()

            # each element in digest is one byte-sized and represents two hexadecimal digits -
            # in other words, the first two elements need to be equal to 0, giving us the first
            # four zero-digits and the third element must be no higher than 0xf ("0f"), so we can
            # get the fifth zero-digit
            has_prefix = digest[0] == 0 and digest[1] == 0 and digest[2] <= 0xf

            if has_prefix:
                result = numkey
                break
        return result

    def part2(self):
        result = 0
        for numkey in itertools.count(start=1):
            md5_input = f'{self.strkey}{str(numkey)}'
            md5_hash = hashlib.md5(md5_input.encode())
            digest = md5_hash.digest()

            has_prefix = digest[0] == 0 and digest[1] == 0 and digest[2] == 0

            if has_prefix:
                result = numkey
                break
        return result

