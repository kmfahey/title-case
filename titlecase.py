#!/usr/bin/python3

"""
This program accepts a stream of titles, one per line, on standard input.
An empty line is printed unaltered. Any other line is taken as a title and
title-cased in a fashion that correctly lowercases certain words.

There's no universally agreed-upon set of rules for title-casing a title. This
program uses the following rules (which roughly agree with the AP Stylebook and
are easily automated):

    * Any single-word article, conjunction, or preposition that's less
      than 4 characters is lowercased.
    * Any multi-word conjunction or preposition that's comprised of
      words all less than 4 characters is lowercased.
    * The first and last words in the title are capitalized, even if they're an 
      article, conjunction, preposition that's less than 4 chars long, or part
      of one.
    * A period-delimited acronym is uppercased.
    * All other words are capitalized.

After being put in title case, the title is printed.
"""

import re
import sys
import argparse


__version__ = "1.0.0"

parser = argparse.ArgumentParser("arachnea")

parser.add_argument("-v", "--version", action="store_true", default=False, dest="show_version",
                    help="Display version information and exit.")

# The lists of articles, [single-word] conjunctions and [single-word]
# prepositions that are lowercased in this program.

articles_lte_4_chars = set(("a", "an", "the"))

conjunctions_lte_4_chars = set(("and", "but", "even", "for", "if", "lest", "nor", "or", "so", "than", "till", "what",
                                "when", "who", "yet"))



prepositions_lte_4_chars = set(("abt", "abt.", "aft", "ago", "amid", "anti", "as", "at", "atop", "away", "away", "back",
                                "bar", "by", "c.", "ca.", "chez", "come", "down", "ere", "from", "from", "here", "home",
                                "if", "in", "into", "into", "less", "lest", "like", "like", "'n'", "’n’", "near",
                                "next", "now", "o'", "o’", "o'er", "o’er", "of", "off", "on", "once", "onto", "out",
                                "over", "oʼ", "oʼer", "past", "per", "plus", "post", "pre", "qua", "re", "sans", "save",
                                "save", "sub", "t'", "t’", "than", "than", "then", "till", "till", "to", "tʼ", "up",
                                "upon", "upon", "v.", "via", "vs.", "w.", "w/", "when", "when", "w/i", "with", "with",
                                "w/o", "ʼnʼ"))

arts_conjs_preps_lte_4_chars = articles_lte_4_chars | conjunctions_lte_4_chars | prepositions_lte_4_chars


# The multi-word conjunctions & prepositions lowercased by this program. They're
# resolved in a separate pass using regex matching against the title after most
# other capitalizations have been done.
multiwd_conj_prep_res = {
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


# Main loop of the utility, when the program is called directly. If -v or
# --version flag was used, prints version information and exits.
#
# Otherwise, iterates over stdin line by line; if a line is empty it's printed
# as-is; otherwise it's taken as a title, put in title case using title_case(),
# and printed.
def main():
    """
    The main loop of the program, when it's called directly. If the -v or --version
    flag was used, prints version information and exits.

    Otherwise, iterates over stdin line by line; if a line is empty it's printed
    as-is; otherwise it's taken as a title, put in title case using title_case(),
    and printed.
    """
    options = parser.parse_args()

    if options.show_version:
        print(f"titlecase.py v.{__version__}. Author: K M Fahey. "
              "Placed in the public domain under The Unlicence <https://unlicense.org/>.")
        exit(0)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            print(line)
        else:
            print(title_case(line))


# str.capitalize() doesn't capitalize the first alpha char in a string if it's
# preceded by non-alpha chars. That's not the behavior desired, so this was
# implemented.
def capitalize(strval):
    """
    Capitalizes the first alphabetic Latin1 character (including accented
    characters) found in the argument, unless it's preceded by one or more numbers.
    If no such character is found the string is returned unmodified. (Used in place
    of str.capitalize(), which doesn't skip over punctuation.)

    :param strval: A string to capitalize the first alphabetic character in.
    :type:         str
    :return:       The string, with its first letter capitalized.
    :rtype:        str
    """
    return re.sub("[^A-Za-zÀ-ÖØ-öø-ÿ0-9]*[A-Za-zÀ-ÖØ-öø-ÿÀ-ÖØ-öø-ÿ]", lambda m: m.group(0).upper(), strval, count=1)


def title_case(strval):
    """
    Applies a title-casing algorithm to the string argument and returns it. In
    order, it capitalizes the first and last words, lowercases all conjunctions and
    prepositions less than 4 characters in length, puts period-delimited acronyms in
    all-caps, and capitalizes all other words.

    :param strval: A string to put in title case with appropriately lowercased
                   words.
    :type:         str
    :return:       The string, put in title case.
    :rtype:        str
    """

    tokens_wordbound_re = re.compile("(?<=[A-Za-zÀ-ÖØ-öø-ÿ0-9._'ʼ’])(?=[^A-Za-zÀ-ÖØ-öø-ÿ0-9._'ʼ’])"
                                         "|"
                                     "(?<=[^A-Za-zÀ-ÖØ-öø-ÿ0-9._'ʼ’])(?=[A-Za-zÀ-ÖØ-öø-ÿ0-9._'ʼ’])")

    tokens = tokens_wordbound_re.split(strval)

    output_list = list()

    # The tokens list is iterated over one at a time, and different types of
    # tokens are handled differently.
    for index in range(len(tokens)):
        token = tokens[index]

        # If the token has the form of a period-delimited acronym (like
        # M.A.S.H.), it's uppercased.
        if re.match(r"^([A-Za-zÀ-ÖØ-öø-ÿ]\.){2,}$", token):
            token = token.upper()

        # If the token has a number as the first alphanumeric substring in the
        # token, followed immediately by the first letter, then it's left as-is.
        # (This avoids capitalizing ordinals like '1st' or '22nd', and all
        # similar tokens.
        elif re.match("^[^A-Za-zÀ-ÖØ-öø-ÿ0-9]*[0-9]+[A-Za-zÀ-ÖØ-öø-ÿ]+", token):
            pass

        # If the token is an article, conjunction, or preposition, it's
        # lowercased.
        elif token.lower() in arts_conjs_preps_lte_4_chars:
            token = token.lower()

        # If the token is word-like and didn't match the previous exclusions,
        # it's capitalized.
        elif re.match("^(?![0-9]+(?:st|nd|rd|th)\b)([A-Za-zÀ-ÖØ-öø-ÿ0-9._'ʼ’]+)$", token):
            token = capitalize(token)

        output_list.append(token)

    output_str = ''.join(output_list)

    # The [rare] phrasal prepositions (like "as well as" or "as per") need to be
    # lowercased but can't be detected using the word-by-word technique the rest
    # of the utility relies on. So after the title has been re-assembled they're
    # grepped for separately.
    for prep_conj_multiwd_str, prep_conj_multiwd_re in multiwd_conj_prep_res.items():
        output_str = prep_conj_multiwd_re.subn(prep_conj_multiwd_str, output_str)[0]

    # If a multi-word preposition is at the beginning (or end) of the title,
    # then its first (or last) word needs to be capitalized, but the remaining
    # words need to be lowercase. Because of this corner case, multi-word
    # conjunction/preposition lowercasing needs to be done *before* first/last
    # word capitalization.
    first_word_plus_punct_re = re.compile("^([^A-Za-zÀ-ÖØ-öø-ÿ0-9._'ʼ’]*)"
                                          "(?![0-9]+(?:st|nd|rd|th))"
                                          "([A-Za-zÀ-ÖØ-öø-ÿ0-9._'ʼ’]+)", re.I)

    last_word_plus_punct_re = re.compile("(?<=[^A-Za-zÀ-ÖØ-öø-ÿ0-9._'ʼ’])"
                                         "(?![0-9]+(?:st|nd|rd|th))"
                                         "([A-Za-zÀ-ÖØ-öø-ÿ0-9._'ʼ’]+)"
                                         "([^A-Za-zÀ-ÖØ-öø-ÿ0-9._'ʼ’]*)$", re.I)

    output_str = first_word_plus_punct_re.subn(lambda m: m.group(1) + capitalize(m.group(2)), output_str)[0]

    output_str = last_word_plus_punct_re.subn(lambda m: capitalize(m.group(1)) + m.group(2), output_str)[0]

    return output_str


if __name__ == "__main__":
    main()
