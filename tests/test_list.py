from fp.list import List
from fp.option import Option
from fp import *


def test_list_is_empty():
    assert List().is_empty()


def test_list_map():
    assert List(1, 2, 3).map(lambda x: x + 1).unwrap() == [2, 3, 4]


def test_list_bind():
    assert List(1, 2, 3).bind(lambda x: List(x + 1, x + 2)).unwrap() == [
        2, 3, 3, 4, 4, 5
    ]


def test_list_filter():
    assert List(1, 2, 3).filter(lambda x: x > 2).unwrap() == [3]


def test_list_intersperse():
    assert List(1, 2, 3).intersperse(0).unwrap() == [1, 0, 2, 0, 3]


def test_list_mkstring():
    assert List(1, 2, 3).mk_string(',') == '1,2,3'


def test_list_sum():
    assert List(1, 2, 3).sum() == 6


def test_list_fold_left():
    assert List(1, 2, 3).fold_left(0, lambda x, y: x - y) == -6


def test_list_fold_right():
    assert List(1, 2, 3).fold_right(0, lambda x, y: x - y) == -6


def test_list_fold():
    assert List(1, 2, 3).fold('A', lambda x, y: x + str(y)) == 'A123'


def test_list_head_option():
    assert List() \
        .head_option() \
        .is_empty()

    assert List(1, 2, 3) \
               .head_option() \
               .get_or_else(0) == 1


def test_list_find():
    assert List(1, 2, 3) \
               .find(lambda x: x == 2) \
               .get_or_else(0) == 2


def test_list_reverse():
    assert List(1, 2, 3).reverse().unwrap() == [3, 2, 1]


def test_from_optional_none():
    assert List.from_optional(None).is_empty()


def test_from_optional_value():
    assert not List.from_optional(1).is_empty()


def test_from_option_none():
    assert List.from_option(Option(None)).is_empty()


def test_from_option_value():
    assert not List.from_option(Option(1)).is_empty()


def test_from_empty_list():
    assert List.from_list([]).is_empty()


def test_from_non_empty_list():
    assert not List.from_list([1, 2, 3]).is_empty()


def test_partition_list_satisfy():
    xs, ys = List(1, 2, 3, 4).partition(lambda x: x <= 2)
    assert xs.unwrap() == [1, 2]
    assert ys.unwrap() == [3, 4]


def test_partition_list_not_satisfy():
    xs, ys = List(1, 2, 3, 4).partition(lambda x: x >= 3)
    assert xs.unwrap() == [3, 4]
    assert ys.unwrap() == [1, 2]


def test_sort_list():
    assert List(3, 2, 1).sorted().unwrap() == [1, 2, 3]


def test_nel_empty():
    assert List().nel().is_empty()
    assert List().nel().fold(List(), identity).unwrap() == []


def test_nel_non_empty():
    assert not List(1, 2, 3).nel()\
                   .fold(List(), identity)\
                   .unwrap() == [1, 2, 3]
