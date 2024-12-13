from config import Day, defaultdict

def is_divisible(a: int, b: int) -> bool:
    return a % b == 0

class Day20(Day):
    def __init__(self, path: str):
        super().__init__(path)
        # target presents
        self.target_presents = int(self.content.strip())

    # Sum of factors is (p1^0 + p1^1 + p1^2 + ...)*(p2^0 + p2^1 + p2^2 + ...)*...
    # for all prime factors and their powers. If we find a dividing prime, we can
    # divide away one of the prime factors completely, then take the sum of factors
    # of the number that's left and multiply it with the sum of the remaining prime's
    # powers.
    def part1(self):
        total_houses = self.target_presents // 10
        primes = [2]
        house_ids = [0, 1, 3]

        house_id = 2
        n_presents = 0
        while n_presents < total_houses:
            house_id += 1
            tmp_presents = 0
            for prime in primes:
                if prime ** 2 > house_id:
                    primes.append(house_id)
                    tmp_presents = house_id + 1
                    break
                elif is_divisible(house_id, prime):
                    # sum of dividing powers
                    # 1 + p + p^2 +... until p^n doesn't divide current
                    prime_original = prime
                    while is_divisible(house_id, prime):
                        prime *= prime_original
                    new_n_presents = (prime - 1) // (prime_original - 1)
                    new_house_id = house_id // (prime // prime_original)
                    tmp_presents = house_ids[new_house_id] * new_n_presents
                    break
            n_presents = tmp_presents
            house_ids.append(n_presents)
        return house_id

    def part2(self):
        total_houses = self.target_presents // 11
        house_visits = 50
        delivery_map = defaultdict(int)
        min_house_id = total_houses
        for elf_id in range(2, total_houses):
            if delivery_map[elf_id] + elf_id >= total_houses:
                min_house_id = elf_id
                break

            for house_id in range(1, house_visits + 1):
                presents = elf_id * house_id
                if presents >= total_houses:
                    break
                delivery_map[presents] += elf_id
        return min_house_id
