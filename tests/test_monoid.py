from fp.monoid import *


def test_int_monoid_zero():
    assert IntMonoid().zero() == 0


def test_int_monoid_append():
    assert IntMonoid().append(1, 2) == 3


def test_string_monoid_zero():
    assert StringMonoid().zero() == ''


def test_string_monoid_append():
    assert StringMonoid().append('a', 'b') == 'ab'
