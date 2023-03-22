#!/usr/bin/python3

import pytest

from titlecase import title_case


def test_simple_case():
    title = "a tramp's wallet stored by an english goldsmith during his wanderings in germany and france"
    title_titlecased = title_case(title)
    assert title_titlecased == "A Tramp's Wallet Stored by an English Goldsmith During His Wanderings in Germany and France"

def test_begins_with_punct():
    title = "...and it comes out here"
    title_titlecased = title_case(title)
    assert title_titlecased == "...And It Comes out Here"

def test_ends_with_punct():
    title = "the delmonico cook book: how to buy food, how to cook it, and how to serve it."
    title_titlecased = title_case(title)
    assert title_titlecased == "The Delmonico Cook Book: How to Buy Food, How to Cook It, and How to Serve It."

def test_has_period_delimited_acronym():
    title = "s.o.s. aphrodite!"
    title_titlecased = title_case(title)
    assert title_titlecased == "S.O.S. Aphrodite!"

