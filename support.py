from config import deepcopy

# taken from https://algocoding.wordpress.com/2015/05/03/next-permutation-in-python-3-4/
def next_permutation(sequence: list):
    size = len(sequence)

    pivot = size - 2
    while pivot >= 0 and sequence[pivot] >= sequence[pivot + 1]:
        pivot -= 1

    if pivot >= 0:
        index = pivot + 1
        while index < size and sequence[index] > sequence[pivot]:
            index += 1
        index -= 1

        sequence[pivot], sequence[index] = sequence[index], sequence[pivot]

        left = pivot + 1
        right = size - 1

        while left < right:
            sequence[left], sequence[right] = sequence[right], sequence[left]
            left += 1
            right -= 1

        return True
    else:
        return False

def permutations(sequence: list):
    result = list()

    if not sequence or len(sequence) == 1:
        result.append(sequence)
    else:
        sequence.sort()
        filtered = set()

        # given a sorted list, a completed set of permutations with the same first element
        # means that any subsequent permutation with that element in the last position is
        # a mirror to one of the existing permutations, i.e. same path, same distance.
        # We skip these by updating our filter with each new element that appears first in
        # a permutation. Once all elements of a permutation are in the filter, we are done.
        while len(filtered) < len(sequence):
            first = sequence[0]
            last = sequence[-1]
            if first not in filtered:
                filtered.add(first)
            if last not in filtered:
                result.append(deepcopy(sequence))
            if not next_permutation(sequence):
                break

    return result
