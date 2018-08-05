from fp.validation import Validation
from fp.option import Option


def test_create_validation_from_option_empty():
    assert Validation.from_option(Option.empty(), 'err').is_failure()


def test_create_validation_from_option_non_empty():
    assert not Validation.from_option(Option.some(1), 'err').is_failure()


def test_fold_from_option_empty():
    assert Validation\
        .from_option(Option.empty(), 'my error message')\
        .fold(lambda x: x, lambda y: y) == 'my error message'


def test_fold_from_option_non_empty():
    assert Validation\
        .from_option(Option.some(1), 'err')\
        .fold(lambda x: x, lambda y: y) == 1
