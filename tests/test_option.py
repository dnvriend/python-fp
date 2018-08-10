from fp.option import Option


def test_option_map():
    assert Option('abc') \
               .map(lambda x: x + 'def') \
               .get_or_else('') == 'abcdef'


def test_option_bind():
    assert Option('abc') \
               .bind(lambda x: Option(x + 'def')).get_or_else('') == 'abcdef'


def test_option_multiple_bind():
    assert Option('abc') \
        .bind(lambda x: Option(x + 'def')) \
        .bind(lambda x: Option(None)) \
        .is_empty()


def test_option_is_defined():
    assert Option('abc').is_defined()
    assert not Option(None).is_defined()


def test_option_is_empty():
    assert Option(None).is_empty()


def test_option_filter():
    assert Option('abc') \
        .filter(lambda x: x == 'abc') \
        .is_defined()

    assert Option('abc') \
        .filter(lambda x: x == 'abcd') \
        .is_empty()


def test_option_mkstring():
    assert Option(None).mk_string() == ''
    assert Option(123).mk_string() == '123'


def test_option_fold():
    assert Option(None) \
               .fold(1, lambda x: x + 1) == 1


def test_non_empty():
    assert not Option.empty().non_empty()


def test_assert_non_empty_on_non_empty():
    assert Option(1).non_empty()
