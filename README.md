# titlecase.py

A simple commandline utility that title-cases text while lowercasing articles, conjunctions and prepositions less than 4 characters, including multi-word conjunctions & prepositions composed of words all less than 4 characters.

# The Algorithm
Accepts a stream of titles, one per line, on standard input. An empty line is printed unaltered. Any other line is taken as a title and title-cased in a fashion that correctly lowercases certain words. After being put in title case, the title is printed.

There's no universally agreed-upon set of rules for title-casing a title. This program adapts the following rules, which have been adapted from [the AP Stylebook's guidelines](https://en.wikipedia.org/wiki/Title_case#AP_Stylebook):

- Any single-word article, conjunction, or preposition that's less than 4 characters is lowercased.
- Any multi-word conjunction or preposition that's comprised of words all less than 4 characters is lowercased.
- The first and last words in the title are capitalized, even if they're a article, conjunction, preposition that's less than 4 chars long, or part of one.
- A period-delimited acronym is uppercased.
- All other words are capitalized.
