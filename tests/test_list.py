from fp.list import List


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
