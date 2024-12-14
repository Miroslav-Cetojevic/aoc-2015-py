from config import Callable, dataclass, Day, Enum, NamedTuple, sys

class RingComboStats(NamedTuple):
    num_rings: int = 0
    rings_cost: int = 0
    bonuses: int = 0

class ComboCost(NamedTuple):
    total_cost: int
    num_rings: int

BonusType = Enum('BonusType', ['dmg', 'ac'])

@dataclass
class Entity:
    health: int
    damage: int
    armor: int

def generate_ring_combos(rings: list):
    combos = [RingComboStats()]
    for i, ring_i in enumerate(rings):
        combos.append(RingComboStats(1, ring_i, i + 1))
        for j in range(i + 1, len(rings)):
            combos.append(RingComboStats(2, ring_i + rings[j], i + j + 2))
    return combos

def precompute_combo_costs(items: list, ring_combos: list):
    max_combo_cost = max(ring_combos, key=lambda combo: combo.bonuses)
    bonus_costs_size = len(items) + max_combo_cost.bonuses
    lookup_array = [[] for _ in range(bonus_costs_size)]
    for i, item_cost in enumerate(items):
        for combo_stats in ring_combos:
            pos = i + combo_stats.bonuses
            total_cost = item_cost + combo_stats.rings_cost
            lookup_array[pos].append(ComboCost(total_cost, combo_stats.num_rings))
    return lookup_array

class Day21v2(Day):
    def __init__(self, path: str):
        super().__init__(path)

        # Player and boss stats
        self.boss = Entity(*(int(line.split()[-1]) for line in self.content.splitlines()))
        self.player_hp = 100

        # shop inventory: the values represent item cost, the dmg & ac values are represented by the
        # index, since they are sequential, but some additional computation will still be needed
        weapons = [8, 10, 25, 40, 74]
        armors = [0, 13, 31, 53, 75, 102]
        rings_dmg = [25, 50, 100]
        rings_ac = [20, 40, 80]

        self.items = [weapons, armors]
        self.ring_groups = [rings_dmg, rings_ac]

        # weapons start with 4 dmg, which will be added when computing with indices
        self.wpn_dmg_offset = len(weapons) - 1
        self.max_num_rings = 2
        self.min_dmg = 1

        # Pre-calculated lookup table
        self.combo_costs = self.create_lookup_table()

    def create_lookup_table(self):
        combo_costs = {}
        bonus_types = [bonus_type for bonus_type in BonusType]
        for typed_rings, typed_items, bonus_type in zip(self.ring_groups, self.items, bonus_types):
            ring_combos = generate_ring_combos(typed_rings)
            typed_combo_costs = precompute_combo_costs(typed_items, ring_combos)
            combo_costs[bonus_type] = typed_combo_costs
        return combo_costs

    def gold_spent(self, start_cost: int, extremum: Callable, must_lose: bool):
        result = start_cost
        dmg_combo_costs = self.combo_costs[BonusType.dmg]
        ac_combo_costs = self.combo_costs[BonusType.ac]
        for i in range(len(dmg_combo_costs)):
            # compute min armor to win
            player_dmg = i + self.wpn_dmg_offset
            player_real_dmg = max(player_dmg - self.boss.armor, self.min_dmg)
            num_rounds_to_win = (self.boss.health // player_real_dmg) + (self.boss.health % player_real_dmg > 0)
            num_rounds_to_last = num_rounds_to_win - 1
            max_hp_loss_per_round = self.player_hp // num_rounds_to_last
            extra_armor = self.player_hp % num_rounds_to_last == 0
            # if player has no hp left after num_rounds_to_last, then they need extra armor
            armor_needed = self.boss.damage - max_hp_loss_per_round + extra_armor - must_lose

            if armor_needed < len(ac_combo_costs):
                for ac_combo_cost in ac_combo_costs[armor_needed]:
                    for dmg_combo_cost in dmg_combo_costs[i]:
                        num_rings = ac_combo_cost.num_rings + dmg_combo_cost.num_rings
                        if num_rings <= self.max_num_rings:
                            new_cost = ac_combo_cost.total_cost + dmg_combo_cost.total_cost
                            result = extremum(result, new_cost)

        return result

    def part1(self):
        return self.gold_spent(start_cost=sys.maxsize, extremum=min, must_lose=False)

    def part2(self):
        return self.gold_spent(start_cost=0, extremum=max, must_lose=True)

