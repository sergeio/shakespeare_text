from collections import defaultdict
from random import random

def make_word(probs):
    """Makes a random word based on the probability dictionary passed in."""

    def get_letter(random_float, cumulative_probs):
        sort_freq = sorted(
            [(value, key) for (key, value) in cumulative_probs.iteritems()])
        for value, key in sort_freq:
            if value < random_float:
                continue
            return key
        assert False

    previous = get_letter(random(), probs['^'])
    letter_lis = [previous]
    previous = '^' + previous

    while previous[-1] != '$':
        new = get_letter(random(), probs[previous])
        letter_lis.append(new)
        previous = previous[-1] + new

    return ''.join(letter_lis[:-1])


def build_count_dict(max_lines=1000):
    """Reads through shakespeare.txt and counts how many times a given letter
    appears after every present two-letter combination.

    """
    def update_count_dict(word, count_dict):
        word = '^' + word.lower() + '$'
        count_dict['^'][word[1]] += 1
        for i in xrange(len(word) - 2):
            count_dict[word[i:i + 2]][word[i + 2]] += 1

    def process_line(line, count_dict):
        line = line.strip()
        if not line:
            return

        for word in line.split(' '):
            if word.upper() == word:
                return
            for char in '()[]':
                if char in word:
                    return
            update_count_dict(word, count_dict)

    defaultdict_int_maker = lambda: defaultdict(int)
    count_dict = defaultdict(defaultdict_int_maker)
    lines_count = 0
    with open('shakespeare.txt', 'r') as text:
        # Skip first 300 lines that contain copyright info
        for i in xrange(300):
            text.next()
        for line in text:
            lines_count += 1
            if lines_count > max_lines:
                break
            process_line(line, count_dict)

    return count_dict

def build_probability_dict(count_dict):
    """Turn a dictionary that counts the frequency of letters into a dictionary
    of probabilities.

    """
    def convert_counts_to_probabilities(counts):
        total = sum(counts.values())
        probabilities = {}
        for key, value in counts.iteritems():
            probabilities[key] = float(value) / float(total)

        return probabilities

    probability_dict = {}
    for key, value in count_dict.iteritems():
        probability_dict[key] = convert_counts_to_probabilities(value)

    return probability_dict


def make_cumulative(probabilities):
    """Takes a dictionary mapping
    {
        character(*): {
            character(**): probability of following the original character(*)
        }
    }

    The function converts these probabilities to cumulative probabilities, in
    order to make it simple to select one character randomly based on its
    probability of following other characters.
    """
    for key, probability_dict in probabilities.iteritems():
        i_sum = 0.0
        for key, value in probability_dict.iteritems():
            probability_dict[key] = i_sum + value
            i_sum += value

def prime_probability_dict(max_lines=100):
    """Creates a useable probability dictionary to be used for generation of
    words.

    """
    count_dict = build_count_dict(max_lines=max_lines)
    probability_dict = build_probability_dict(count_dict)
    make_cumulative(probability_dict)

    return probability_dict

def make_paragraph(probs, num_words=200):
    """Generates a paragraph of ``num_words`` words based on the probability
    dictionary passed in.

    """
    def handle_periods(paragraph, i):
        """Capitalize the beginnings of sentences."""

        if paragraph[i] in '.?!':
            try:
                paragraph[i + 2] = paragraph[i + 2].upper()
            except IndexError:
                pass

    def handle_i(paragraph, i):
        """handle making all the appropriate i's uppercase.

        The parameter ``i`` should never be 0, since we raise that to uppercase
        first.

        """
        if paragraph[i - 1] == ' ' and paragraph[i + 1] in ' \'':
            paragraph[i] = 'I'

    def handle_end_punctuation(paragraph):
        """Adds a period to the end of the paragraph if appropriate."""

        letter = paragraph[-1]
        if letter in '!.?':
            return
        if letter in ',;':
            paragraph[-1] = '.'
        else:
            paragraph.append('.')

    paragraph = list(' '.join([make_word(probs) for i in xrange(num_words)]))
    paragraph[0] = paragraph[0].upper()
    for i, letter in enumerate(paragraph):
        handle_periods(paragraph, i)
        handle_i(paragraph, i)
    handle_end_punctuation(paragraph)
    return ''.join(paragraph)
