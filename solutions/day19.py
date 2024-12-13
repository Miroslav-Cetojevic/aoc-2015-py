from config import Day, re

class Day19(Day):
    def __init__(self, path: str):
        super().__init__(path)

        lines = self.content.splitlines()
        self.rules = [(src, dest) for src, dest in (line.split(' => ') for line in lines[:-2])]
        self.medicine = lines[-1]
        self.molecules = re.findall(r'[A-Z][a-z]*', self.medicine)

    def part1(self):
        distinct_molecules = set()
        for src, dest in self.rules:
            # Find all occurrences of the source string in the molecule
            start = 0
            while (index := self.medicine.find(src, start)) != -1:
                # Replace the found occurrence with the destination string
                new_molecule = f'{self.medicine[:index]}{dest}{self.medicine[index + len(src):]}'
                distinct_molecules.add(new_molecule)
                # Continue searching after this occurrence
                start = index + 1
        return len(distinct_molecules)

    def part2(self):
        # Formula: for each step add (1 - n_parentheses - n_commas)
        # The formula calculates the steps as follows:
        # 1. Each uppercase element contributes 1 step.
        # 2. "Rn" and "Ar" do not represent actual steps, so they subtract 1 step each.
        # 3. "Y" introduces branching, effectively subtracting 2 steps per occurrence.
        # 4. Subtracting 1 at the end accounts for the final transformation to "e".
        n_steps = sum((1 - (molecule in ('Rn', 'Ar')) - 2 * (molecule == 'Y'))
                      for molecule in self.molecules)
        return n_steps - 1

