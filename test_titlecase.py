#!/usr/bin/python3

import pytest

from titlecase import title_case


def test_simple_case():
    title = "a tramp's wallet stored by an english goldsmith during his wanderings in germany and france"
    titlecased = title_case(title)
    assert titlecased == "A Tramp's Wallet Stored by an English Goldsmith During His Wanderings in Germany and France"

def test_begins_with_punct():
    title = "...and it comes out here"
    titlecased = title_case(title)
    assert titlecased == "...And It Comes out Here"

def test_ends_with_punct():
    title = "the delmonico cook book: how to buy food, how to cook it, and how to serve it."
    titlecased = title_case(title)
    assert titlecased == "The Delmonico Cook Book: How to Buy Food, How to Cook It, and How to Serve It."

def test_has_period_delimited_acronym():
    title = "s.o.s. aphrodite!"
    titlecased = title_case(title)
    assert titlecased == "S.O.S. Aphrodite!"

def test_has_multi_word_preposition_general_case():
    title = "in and out of rebel prisons"
    titlecased = title_case(title)
    assert titlecased == "In and out of Rebel Prisons"

def test_has_multi_word_preposition_at_beginning():
    title = "out of the hurly-burly; or, life in an odd corner"
    titlecased = title_case(title)
    assert titlecased == "Out of the Hurly-Burly; or, Life in an Odd Corner"

def test_has_multi_word_preposition_at_end():
    title = "entering the city with the horse i got off of"
    titlecased = title_case(title)
    assert titlecased == "Entering the City With the Horse I Got off Of"

def test_has_accented_character_general_case():
    title = "pascal's pensées"
    titlecased = title_case(title)
    assert titlecased == "Pascal's Pensées"

def test_has_accented_character_at_word_start():
    title = "pascal's pensées"
    titlecased = title_case(title)
    assert titlecased == "Pascal's Pensées"

def test_has_accented_character_at_word_start():
    title = "on conducting (Üeber das dirigiren): a treatise on style in the execution of classical music"
    titlecased = title_case(title)
    assert titlecased == "On Conducting (Üeber Das Dirigiren): a Treatise on Style in the Execution of Classical Music"



