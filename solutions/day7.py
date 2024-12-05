from config import Day, deepcopy, NamedTuple, StrEnum

Gate = StrEnum('Gate', ['AND', 'OR', 'LSHIFT', 'RSHIFT', 'NOT'])

class Operation(NamedTuple):
    op1: str = ''
    gate: str = ''
    op2: str = ''

class Day7(Day):
    def __init__(self, path: str):
        super().__init__(path)
        # === needed for part 2 === #
        self.result_part1 = None
        # ========================= #
        self.gate_map = {
            Gate.AND: lambda op1, op2: op1 & op2,
            Gate.OR: lambda op1, op2: op1 | op2,
            Gate.LSHIFT: lambda op1, op2: op1 << op2,
            Gate.RSHIFT: lambda op1, op2: op1 >> op2,
            Gate.NOT: lambda op1, _: ~op1,
            '': lambda op1, _: op1,
        }
        self.ops = dict()
        for line in self.content.splitlines():
            tokens = [token for token in line.split(' ')]
            wire = tokens[-1]
            # length of tokens tells us what kind of operation it is
            match len(tokens):
                # confusingly, StrEnum automatically lower-cases its elements even if they
                # are written in upper-case, so the tokens have to match that behavior
                case 5: self.ops[wire] = Operation(op1=tokens[0], gate=tokens[1].lower(), op2=tokens[2])
                case 4: self.ops[wire] = Operation(op1=tokens[1], gate=tokens[0].lower())
                case 3: self.ops[wire] = Operation(op1=tokens[0])

    def run_circuit(self, ops):
        circuit = dict()

        def get_signal(op, is_signal, is_mapped):
            value = 0
            if is_signal:
                value = int(op)
            elif is_mapped:
                value = circuit[op]
            return value

        while ops.items():
            for wire, operation in list(ops.items()):
                op1, gate, op2 = operation

                is_op1_signal = op1.isnumeric()
                is_op2_signal = op2.isnumeric()

                is_op1_mapped = not is_op1_signal and op1 in circuit
                is_op2_mapped = not is_op2_signal and op2 in circuit

                is_op2_empty = ''.__eq__(op2)

                is_op1_actionable = is_op1_signal or is_op1_mapped
                is_op2_actionable = is_op2_signal or is_op2_mapped or is_op2_empty

                if is_op1_actionable and is_op2_actionable:
                    op1_signal = get_signal(op1, is_op1_signal, is_op1_mapped)
                    op2_signal = get_signal(op2, is_op2_signal, is_op2_mapped)

                    # do operation associated with the current gate
                    circuit[wire] = self.gate_map[gate](op1_signal, op2_signal)

                    # operation no longer needed
                    del ops[wire]

        return circuit['a']

    def part1(self):
        # deepcopy is necessary, as run_circuit() will modify the dictionary,
        # thus making the resulting dict unusable for part 2 and subsequent
        # iterations in the main function
        self.result_part1 = self.run_circuit(deepcopy(self.ops))
        return self.result_part1

    def part2(self):
        # see part 1 for why deepcopy is used
        ops = deepcopy(self.ops)
        ops['b'] = Operation(op1=str(self.result_part1))
        return self.run_circuit(ops)
