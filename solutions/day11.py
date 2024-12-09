from config import Day

class Day11(Day):
    def __init__(self, path: str):
        super().__init__(path)
        print(self.content)
        self.password = self.content.strip()
        self.pwdlen = len(self.password)
        self.pwdlen_less1 = self.pwdlen - 1
        self.pwdlen_less2 = self.pwdlen - 2
        self.callables = [list,
                          self.find_next_valid_password,
                          self.get_next_password,
                          self.find_next_valid_password]

    def has_incr_triple(self, password: list[str]):
        for i in range(self.pwdlen_less2):
            if (ord(password[i]) + 1 == ord(password[i + 1])
                and ord(password[i + 1]) + 1 == ord(password[i + 2])):
                return True
        return False

    def has_two_pairs(self, password: list[str]):
        count = 0
        i = 1
        while i < self.pwdlen:
            if password[i] == password[i - 1]:
                count += 1
                if count == 2:
                    return True
                i += 2
            else:
                i += 1
        return False

    def valid(self, password: list[str]):
        is_not_banned = True
        for c in password:
            if c in 'ilo':
                is_not_banned = False
                break
        return (is_not_banned
                and self.has_incr_triple(password)
                and self.has_two_pairs(password))

    def get_next_password(self, password: list[str]):
        i = self.pwdlen_less1
        while password[i] == 'z':
            password[i] = 'a'
            i -= 1
        password[i] = chr(ord(password[i]) + 1)
        return password

    def find_next_valid_password(self, password: list[str]):
        while not self.valid(password):
            password = self.get_next_password(password)
        return password

    def part1(self):
        return ''.join(self.find_next_valid_password(list(self.password)))

    def part2(self):
        password = self.password
        for func in self.callables:
            password = func(password)
        return ''.join(password)
