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
