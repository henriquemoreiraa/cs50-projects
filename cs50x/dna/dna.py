import csv
import sys

strs_l = {'AGATC': 0,'TTTTTTCT': 0,'AATG': 0,'TCTAG': 0,'GATA': 0,'TATC': 0,'GAAA': 0,'TCTG': 0}
strs_s = {'AGATC': 0,'AATG': 0,'TATC': 0}

def main():
    strs = {}

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # TODO: Read database file into a variable
    people = []

    with open(sys.argv[1]) as file:
        if sys.argv[1] == 'databases/large.csv':
            strs = strs_l
        else:
            strs = strs_s

        reader = csv.DictReader(file)
        for data in reader:
            people += [data]

    # TODO: Read DNA sequence file into a variable
    dna = None

    with open(sys.argv[2]) as file:
        dna = file.read()

    # TODO: Find longest match of each STR in DNA sequence
    # dna_len = len(dna)
    # sequences = []
    # count = 0

    for str in strs:
        strs[str] = longest_match(dna, str)

    # for i in range(dna_len):
    #     for j in range(dna_len):
    #         str = dna[i:j]
    #         if str in strs:
                # if len(sequences) > 0 and sequences[len(sequences) - 1] == str:
                #     count += 1
                # else:
                #     sequences += [str]
                #     count = 1
                # if strs[str] < count:
                #     print(count)
                #     strs[str] = count

    # TODO: Check database for matching profiles
    person = 'No match'

    for data in people:
        if person != 'No match':
            break
        for key in strs:
            if int(strs[key]) == int(data[key]):
                person = data['name']
            else:
                person = 'No match'
                break

    print(person)

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
