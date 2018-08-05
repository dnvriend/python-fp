from __future__ import annotations

from typing import TypeVar, Generic, Callable
from fp.option import Option

A = TypeVar('A')
B = TypeVar('B')


class List(Generic[A]):

    def __init__(self, *xs: A):
        self.xs = list(xs)

    def map(self, f: Callable[[A], B]) -> List[B]:
        return List(*[f(x) for x in self.xs])

    def bind(self, f: Callable[[A], List[B]]) -> List[B]:
        ys: List[B] = []
        for x in self.xs:
            ys += f(x).unwrap()
        return List(*ys)

    def for_each(self, f: Callable[[A], None]) -> None:
        [f(x) for x in self.xs]
        return None

    def filter(self, f: Callable[[A], bool]) -> List[A]:
        return List(*[x for x in self.xs if f(x)])

    def is_empty(self) -> bool:
        return len(self.xs) == 0

    def mk_string(self, sep: str = '') -> str:
        return self.map(lambda x: str(x)) \
            .intersperse(sep) \
            .fold('', lambda x, y: x + y)

    def intersperse(self, y: A) -> List[A]:

        def iterator():
            it = iter(self.xs)
            yield next(it)
            for x in it:
                yield y
                yield x

        return List(*iterator())

    def fold_left(self, zero: A, f: Callable[[A, A], B]) -> B:
        """Catamorphism to A, from left to right"""
        accum: A = zero
        for x in self.xs:
            accum = f(accum, x)
        return accum

    def fold_right(self, zero: A, f: Callable[[A, A], B]) -> B:
        """Catamorphism to A, from right to left"""
        return List(*reversed(self.xs)).fold_left(zero, f)

    def fold(self, zero: B, f: Callable[[B, A], B]) -> B:
        """Catamorphism to B from left to right"""
        accum: B = zero
        for x in self.xs:
            accum = f(accum, x)
        return accum

    def find(self, f: Callable[[A], bool]) -> Option[A]:
        """Returns the first value that matches the predicate"""
        return self.filter(f).head_option()

    def head_option(self) -> Option[A]:
        """Returns the first element, if available"""
        if self.is_empty():
            return Option(None)
        else:
            return Option(self.xs[0])

    def reverse(self) -> List[A]:
        return List(*reversed(self.xs))

    def sum(self) -> A:
        return sum(self.xs)

    def length(self) -> int:
        return len(self.xs)

    def unwrap(self):
        """Returns the underlying list"""
        return self.xs

    def __str__(self):
        return f'List({self.xs})'
