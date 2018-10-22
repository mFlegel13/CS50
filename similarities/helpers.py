from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""

    alines = set(a.split("\n"))
    blines = set(b.split("\n"))

    return alines & blines


def sentences(a, b):
    """Return sentences in both a and b"""

    asentences = set(sent_tokenize(a))
    bsentences = set(sent_tokenize(b))

    return asentences & bsentences

def substring_tokenize(str, n):

    substrings = []

    for i in range(len(str) - n + 1):
        substrings.append(str[i:i + n])

    return substrings

def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    asub = set(substring_tokenize(a, n))
    bsub = set(substring_tokenize(b, n))

    return asub & bsub
