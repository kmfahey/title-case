#!/usr/bin/python3

"""
Accepts a stream of lines on stdin, or a single line as commandline arguments,
and applies a grammatically correct title-casing algorithm to it. The first and
last words are capitalized, as is every word that isn't an article, conjunction
or preposition (or part of a preposition for the few multi-word prepositions).
"""

import re
import sys
import functools

# A list of the words that should be lowercased in a title. This list is not
# authoritative; several competing lists were found. But this list seemed the
# most inclusive. Note that variations on 'n' have been added, so a title like
# Toys 'n' Games is capitalized properly.
arts_conjs_preps = set(("a", "amid", "an", "and", "and", "anti", "as", "at", "atop", "away", "but", "but", "by", "cum",
                        "down", "for", "for", "from", "gone", "in", "into", "less", "'n", "n'", "'n'", "ʼn", "nʼ",
                        "ʼnʼ", "’n", "n’", "’n’", "nor", "off", "on", "onto", "or", "out", "over", "past", "per", "pro",
                        "save", "so", "than", "the", "to", "up", "via", "with", "yet"))

# These multi-word prepositions are resolved in a separate pass after the title
# has been reassembled as a str. This dict re-compiles all the regexes that pass
# will use.
prep_phrase_res = {
    "as for": re.compile("as for", re.I),
    "as per": re.compile("as per", re.I),
    "as well as": re.compile("as well as", re.I),
    "away from": re.compile("away from", re.I),
    "but for": re.compile("but for", re.I),
    "due to": re.compile("due to", re.I),
    "far from": re.compile("far from", re.I),
    "in case of": re.compile("in case of", re.I),
    "in face of": re.compile("in face of", re.I),
    "in view of": re.compile("in view of", re.I),
    "near to": re.compile("near to", re.I),
    "off of": re.compile("off of", re.I),
    "out of": re.compile("out of", re.I),
}

# An elaborated regex for matching on the border between a word token and a non-word token.
tokens_wordbound_re = re.compile("(?<=[A-Za-zÀ-ÿ0-9._'ʼ’])(?=[^A-Za-zÀ-ÿ0-9._'ʼ’])"
                                     "|"
                                 "(?<=[^A-Za-zÀ-ÿ0-9._'ʼ’])(?=[A-Za-zÀ-ÿ0-9._'ʼ’])")


def main():
    lines = list(sys.stdin)
    if lines:
        for line in lines:
            line = line.strip()
            if not line:
                print()
            else:
                print(title_case(line))
    else:
        line = " ".join(sys.argv[1:])
        print(title_case(line))


# str.capitalize() doesn't capitalize the first alpha char in a string if it's
# preceded by non-alpha chars. That's not the behavior desired, so this was
# implemented.
def capitalize(strval):
    return re.sub("[A-Za-zÀ-ÿ]", lambda m: m.group(0).upper(), strval, count=1)


# Matching a length of characters considered as a word-like token. Includes three
# different apostrophes so contractions parse as one token. So is a period, so
# period-delimited acronyms parse as one token. Note the range 'À-ÿ', which
# includes all accented characters in the latin1 page.
def is_unic_alnum_punct(strval):
    return re.match("^[A-Za-zÀ-ÿ0-9._'ʼ’]+$", strval)


# Matches ordinals like 1st, 2nd, 3rd, etc.
def is_ordinal_num(strval):
    return re.match("^[0-9]+(st|nd|rd|th)$", strval, re.I)


def title_case(strval):
    tokens = tokens_wordbound_re.split(strval)

    output_list = list()

    # The tokens list is iterated over one at a time, and different types of
    # tokens are handled differently.
    for index in range(len(tokens)):
        token = tokens[index]
        # If the token has the form of a period-delimited acronym (like
        # M.A.S.H.), it's uppercased.
        if re.match(r"^([A-Za-zÀ-ÿ]\.){2,}$", token):
            token = token.upper()
        # If the token is an article, conjunction, or preposition, it's
        # lowercased.
        elif token.lower() in arts_conjs_preps:
            token = token.lower()
        # If the token is word-like and didn't match the previous exclusions,
        # it's capitalized.
        elif re.match("^([à-ÿa-z'’ʼ]+)$", token):
            token = capitalize(token)
        output_list.append(token)

    output_str = ''.join(output_list)

    # The [rare] phrasal prepositions (like "as well as" or "as per") need to be
    # lowercased but can't be detected using the word-by-word technique the rest
    # of the utility relies on. So after the title has been re-assembled they're
    # grepped for separately.
    for prep_phrase_str, prep_phrase_re in prep_phrase_res.items():
        output_str = prep_phrase_re.subn(prep_phrase_str, output_str)[0]

    # If a phrasal preposition is at the beginning (or end) of the title, then
    # its first (or last) word needs to be capitalized, but the remaining words
    # need to be lowercase. Because of this corner case the program doesn't
    # address 1st/last word capitalization til now.
    first_word_plus_punct_re = re.compile("^([^A-Za-zÀ-ÿ0-9._'ʼ’]*)"
                                          "(?![0-9]+(?:st|nd|rd|th))"
                                          "([A-Za-zÀ-ÿ0-9._'ʼ’]+)", re.I)
    last_word_plus_punct_re = re.compile("(?<=[^A-Za-zÀ-ÿ0-9._'ʼ’])"
                                         "(?![0-9]+(?:st|nd|rd|th)
                                         "([A-Za-zÀ-ÿ0-9._'ʼ’]+)"
                                         "([^A-Za-zÀ-ÿ0-9._'ʼ’]*)$", re.I)
    output_str = first_word_plus_punct_re.subn(lambda m: m.group(1) + capitalize(m.group(2)), output_str)[0]
    output_str = last_word_plus_punct_re.subn(lambda m: capitalize(m.group(1)) + m.group(2), output_str)[0]

    return output_str


if __name__ == "__main__":
    main()
