from config import Callable, ceil, combinations, Day, NamedTuple, operator, product, sys

class Entity(NamedTuple):
    health: int
    damage: int
    armor: int

class Item(NamedTuple):
    price: int = 0
    dmg_bonus: int = 0
    ac_bonus: int = 0

class Day21(Day):
    def __init__(self, path: str):
        super().__init__(path)
        self.boss = Entity(*(int(line.split()[-1]) for line in self.content.splitlines()))
        self.hero_hp = 100
        weapons = [Item(8, 4, 0), Item(10, 5, 0), Item(25, 6, 0), Item(40, 7, 0), Item(74, 8, 0)]
        armors = [Item(), Item(13, 0, 1), Item(31, 0, 2), Item(53, 0, 3), Item(75, 0, 4), Item(102, 0, 5)]
        rings = [Item(), Item(25,1,0), Item(50,2,0), Item(100,3,0), Item(20,0,1), Item(40,0,2), Item(80,0,3)]
        ring_pairs = list(combinations(rings, 2))
        self.items = [weapons, armors, ring_pairs]
        self.combos = list(self.all_combos())
        self.targets = {'min': (sys.maxsize, operator.ge, min),
                        'max': (0, operator.lt, max)}

    def all_combos(self):
        for w, a, (r1, r2) in product(*self.items):
            yield w, a, r1, r2

    def gold_spent(self, start: int, cmp: Callable, chooser: Callable):
        result = start
        hero_hp = self.hero_hp
        boss = self.boss
        for combo in self.combos:
            cost = dmg = ac = 0
            for item in combo:
                cost += item.price
                dmg += item.dmg_bonus
                ac += item.ac_bonus

            hero_dmg = max(dmg - boss.armor, 1)
            boss_dmg = max(boss.damage - ac, 1)

            hero_rounds = ceil(hero_hp / boss_dmg)
            boss_rounds = ceil(boss.health / hero_dmg)

            if cmp(hero_rounds, boss_rounds):
                result = chooser(result, cost)

        return result

    def part1(self):
        return self.gold_spent(*self.targets['min'])

    def part2(self):
        return self.gold_spent(*self.targets['max'])
