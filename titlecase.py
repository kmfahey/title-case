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

# There's no single standard grammatical answer to the question "Which words
# need to be lowercased in a title?" Worse yet, most of the answers that *do*
# exist would require a grammar parser to implement since some of their rules
# depend on identifying the grammatical class of adjacent words. This program
# implements the following simple rules:
# 
# * Capitalize the first and last words in the title.
# * Capitalize every letter in a period-delimited acronym.
# * Lowercase any single-word article, conjunction, or preposition that's less
#   than 4 characters.
# * Lowercase any multi-word conjunction or preposition that's comprised of
#   words all less than 4 characters.
# * Capitalize all other words.


# The lists of articles, [single-word] conjunctions and [single-word]
# prepositions that are lowercased in this program.

articles_lt_4_chars = set(("a", "an", "the"))
conjunctions_lt_4_chars = set(("and", "but", "for", "if", "nor", "or", "so", "who", "yet"))
prepositions_lt_4_chars = set(("abt.", "aft", "ago", "as", "at", "bar", "by", "c.", "ca.", "ere", "if", "in", "'n'",
                               "’n’", "ʼnʼ", "now", "o'", "o’", "o'er", "o’er", "of", "off", "on", "out", "oʼ", "oʼer",
                               "per", "pre", "qua", "re", "sub", "t'", "t’", "to", "tʼ", "up", "v.", "via", "vs.", "w.",
                               "w/", "w/i", "w/o"))

arts_conjs_preps = articles_lt_4_chars | conjunctions_lt_4_chars | prepositions_lt_4_chars


# The multi-word conjunctions & prepositions lowercased by this program. They're
# resolved in a separate pass using regex matching against the title after most
# other capitalizations have been done.
multiw_conj_prep_res = {
    "à la": re.compile(r"\bà la\b", re.I),
    "as if": re.compile(r"\bas if\b", re.I),
    "as for": re.compile(r"\bas for\b", re.I),
    "as of": re.compile(r"\bas of\b", re.I),
    "as per": re.compile(r"\bas per\b", re.I),
    "as to": re.compile(r"\bas to\b", re.I),
    "but for": re.compile(r"\bbut for\b", re.I),
    "due to": re.compile(r"\bdue to\b", re.I),
    "off of": re.compile(r"\boff of\b", re.I),
    "out of": re.compile(r"\bout of\b", re.I),
    "per pro": re.compile(r"\bper pro\b", re.I),
    "up to": re.compile(r"\bup to\b", re.I),
    "vis-à-vis": re.compile(r"\bvis-à-vis\b", re.I)
}


# Main loop of the utility, when the program is called directly. Iterates over
# stdin line by line; if a line is empty an empty line printed; otherwise the
# line is put in title case with title_case() and printed.
def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            print()
        else:
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
    # An elaborated regex for matching on the border between a word token and a
    # non-word token.
    tokens_wordbound_re = re.compile("(?<=[A-Za-zÀ-ÿ0-9._'ʼ’])(?=[^A-Za-zÀ-ÿ0-9._'ʼ’])"
                                         "|"
                                     "(?<=[^A-Za-zÀ-ÿ0-9._'ʼ’])(?=[A-Za-zÀ-ÿ0-9._'ʼ’])")

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
    for prep_phrase_str, prep_phrase_re in multiw_conj_prep_res.items():
        output_str = prep_phrase_re.subn(prep_phrase_str, output_str)[0]

    # If a phrasal preposition is at the beginning (or end) of the title, then
    # its first (or last) word needs to be capitalized, but the remaining words
    # need to be lowercase. Because of this corner case the program doesn't
    # address 1st/last word capitalization til now.
    first_word_plus_punct_re = re.compile("^([^A-Za-zÀ-ÿ0-9._'ʼ’]*)"
                                          "(?![0-9]+(?:st|nd|rd|th))"
                                          "([A-Za-zÀ-ÿ0-9._'ʼ’]+)", re.I)

    last_word_plus_punct_re = re.compile("(?<=[^A-Za-zÀ-ÿ0-9._'ʼ’])"
                                         "(?![0-9]+(?:st|nd|rd|th))"
                                         "([A-Za-zÀ-ÿ0-9._'ʼ’]+)"
                                         "([^A-Za-zÀ-ÿ0-9._'ʼ’]*)$", re.I)

    output_str = first_word_plus_punct_re.subn(lambda m: m.group(1) + capitalize(m.group(2)), output_str)[0]
    output_str = last_word_plus_punct_re.subn(lambda m: capitalize(m.group(1)) + m.group(2), output_str)[0]

    return output_str


if __name__ == "__main__":
    main()
