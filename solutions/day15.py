from config import Day

# n = number of ingredients
# total = how many teaspoons of all ingredients together
def mixtures(n_ingredients, n_teaspoons):
    start = n_teaspoons if n_ingredients == 1 else 0
    for i in range(start, n_teaspoons + 1):
        countdown = n_ingredients - 1
        if countdown:
            for y in mixtures(countdown, n_teaspoons - i):
                yield [i] + y
        else:
            yield [i]

class Day15(Day):
    def __init__(self, path: str):
        super().__init__(path)
        self.ingredients = [[int(token.split()[1])
                             for token in line.replace(', ', ',').split(': ')[1].split(',')]
                            for line in self.content.splitlines()]
        self.n_ingredients = len(self.ingredients)
        self.n_properties = len(self.ingredients[0][:-1])
        self.n_teaspoons = 100

    def part1(self):
        max_score = 0

        for recipe in mixtures(self.n_ingredients, self.n_teaspoons):
            tmp_score = 1
            for i in range(self.n_properties):
                property_score = 0
                for j in range(self.n_ingredients):
                    property_score += recipe[j] * self.ingredients[j][i]
                if property_score < 0:
                    tmp_score = 0
                    break  # No need to calculate further
                tmp_score *= property_score
            max_score = max(max_score, tmp_score)
        return max_score

    def part2(self):
        max_score = 0

        for recipe in mixtures(self.n_ingredients, self.n_teaspoons):
            tmp_score = 1
            valid = True
            for i in range(self.n_properties):
                property_score = 0
                for j in range(self.n_ingredients):
                    property_score += recipe[j] * self.ingredients[j][i]
                if property_score < 0:
                    valid = False
                    break  # No need to calculate further
                tmp_score *= property_score

            if valid:
                calories = 0
                for j in range(self.n_ingredients):
                    calories += recipe[j] * self.ingredients[j][-1]
                if calories == 500:
                    max_score = max(max_score, tmp_score)
        return max_score
