# Problem Set 4A
# Name: Chase Zelechowski
# Collaborators:
# Time Spent: all permutations of 6:00

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
    if len(sequence) <= 1:
        return [sequence]
    new_perms = []
    for i in range(len(sequence)):
        permutations = get_permutations(sequence[:i]+sequence[i+1:])
        new_perms = new_perms + [sequence[i] + perm for perm in permutations]
    return new_perms


if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)
    example_1 = 'cat'
    print('Input:', example_1)
    print('Expected Output:', ['cat', 'cta', 'act', 'atc', 'tca', 'tac'])
    print('Actual Output:', get_permutations(example_1))

    example_2 = 'dog'
    print('Input:', example_2)
    print('Expected Output:', ['dog', 'dgo', 'odg', 'ogd', 'gdo', 'god'])
    print('Actual Output:', get_permutations(example_2))

    example_3 = 'bat'
    print('Input:', example_3)
    print('Expected Output:', ['bat', 'bta', 'abt', 'atb', 'tba', 'tab'])
    print('Actual Output:', get_permutations(example_3))

