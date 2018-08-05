from fp.string import *


def test_parse_int_failure():
    assert parse_int('a').is_failure()


def test_parse_int_success():
    assert parse_int(1).is_success()


def test_parse_float_failure():
    assert parse_float('a').is_failure()


def test_parse_float_success():
    assert parse_float('1.0').is_success()


def test_parse_bool_success():
    assert parse_boolean('').is_success()
    assert parse_boolean('a').is_success()
    assert parse_boolean('0').is_success()
    assert parse_boolean('1').is_success()
