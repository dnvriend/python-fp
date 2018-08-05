from fp.validation import Validation
from fp.option import Option
from fp.list import List
from fp import identity


def test_create_validation_from_option_empty():
    assert Validation.from_option(Option.empty(), 'err').is_failure()


def test_create_validation_from_option_non_empty():
    assert not Validation.from_option(Option.some(1), 'err').is_failure()


def test_fold_from_option_empty():
    assert Validation \
               .from_option(Option.empty(), 'my error message') \
               .fold(identity, identity) == 'my error message'


def test_fold_from_option_non_empty():
    assert Validation \
               .from_option(Option.some(1), 'err') \
               .fold(identity, identity) == 1


def test_validation_sequence_failure():
    assert Validation \
               .sequence(List(Validation.failure('a'), Validation.failure('b'), Validation.failure('c'))) \
               .fold(lambda err: err, lambda x: x) \
               .unwrap() == ['a', 'b', 'c']


def test_validation_sequence_success():
    assert Validation \
               .sequence(List(Validation.success(1), Validation.success(2), Validation.success(3))) \
               .fold(identity, identity) \
               .unwrap() == [1, 2, 3]


def test_validation_sequence_with_success_and_failure():
    assert Validation \
               .sequence(
        List(Validation.success(1), Validation.failure('err1'), Validation.success(3), Validation.failure('err2'))) \
               .fold(identity, identity) \
               .unwrap() == ['err1', 'err2']


def test_validation_example():
    fn = Validation.from_option(Option(None), 'first name is empty')
    ln = Validation.from_option(Option(None), 'last name is empty')
    age = Validation.from_option(Option(None), 'age is empty')
    zip = Validation.from_option(Option(None), 'zipcode is empty')
    assert Validation.sequence(List(fn, ln, age, zip)) \
        .fold(identity, identity) \
        .unwrap() == ['first name is empty', 'last name is empty', 'age is empty', 'zipcode is empty']
