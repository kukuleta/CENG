# Problem Set 4A
# Name: <Ismail Denizli>
def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    if len(sequence) == 1:
        return [sequence]
    possibleSeq = []
    results = []
    for i in range(len(sequence + sequence[:-1]) // 2 + 1):
        possibleSeq.append((sequence + sequence[:-1])[i: len(sequence + sequence[:-1]) // 2 + 1 + i])
    for x in possibleSeq:
        results += [[x[0]] + [get_permutations(x[1:len(x)])]]
    return [subOrder[0] + index for subOrder in results for index in subOrder[1]]

if __name__ == '__main__':
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a
#    sequence of length n)
    assert get_permutations("a") == ['a'], "Re-ordering one letter should be identical to itself."
    assert get_permutations("ab") == ['ab','ba'], "Implementation failed to re-order the sequence 'ab'"
    assert get_permutations("abc") == ['abc', 'acb', 'bca', 'bac', 'cab', 'cba'],"Implementation failed to re-order the sequence 'abc'"
