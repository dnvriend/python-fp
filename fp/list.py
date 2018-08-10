from __future__ import annotations

from typing import TypeVar, Generic, Callable, List as PList, Optional, Tuple
from fp.option import Option
from fp.monoid import Monoid, StringMonoid

A = TypeVar('A')
B = TypeVar('B')


class List(Generic[A]):

    def __init__(self, *xs: A):
        self.xs = list(xs)

    @classmethod
    def from_list(cls, xs: PList[A]) -> List[A]:
        return List(*xs)

    @classmethod
    def from_optional(cls, x: Optional[A]) -> List[A]:
        return List.from_option(Option(x))

    @classmethod
    def from_option(cls, x: Option[A]) -> List[A]:
        return x.fold(List(), lambda y: List(y))

    @classmethod
    def empty(cls) -> List[A]:
        return List()

    def map(self, f: Callable[[A], B]) -> List[B]:
        """Converts any element of the list from A to B ie. F[A] -> F[B]"""
        return List(*[f(x) for x in self.xs])

    def fold_map(self, m: Monoid[B], f: Callable[[A], B]) -> B:
        """First 'map' each element of the List to B, and then 'fold' the List to B according to the Monoid[B]"""
        return self.map(f).fold(m.zero(), m.append)

    def bind(self, f: Callable[[A], List[B]]) -> List[B]:
        """Natural Transformation of an endofunctor ie. F[F[A]] -> F[A]"""
        ys: List[B] = []
        for x in self.xs:
            ys += f(x).unwrap()
        return List(*ys)

    def foreach(self, f: Callable[[A], None]) -> None:
        [f(x) for x in self.xs]
        return None

    def filter(self, f: Callable[[A], bool]) -> List[A]:
        return List.from_list(list(filter(f, self.xs)))

    def is_empty(self) -> bool:
        return len(self.xs) == 0

    def mk_string(self, sep: str = '') -> str:
        if self.is_empty():
            return StringMonoid().zero()

        return self.map(lambda x: str(x)) \
            .intersperse(sep) \
            .foldl(StringMonoid())

    def intersperse(self, y: A) -> List[A]:
        """Intersperse the list with a value 'y'"""

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

    def foldl(self, m: Monoid[A]) -> A:
        """Catamorphism to A, from left to right with Monoid[A]"""
        return self.fold_left(m.zero(), m.append)

    def foldr(self, m: Monoid[A]) -> A:
        """Catamorphism to A, from right to left with Monoid[A]"""
        return self.fold_right(m.zero(), m.append)

    def find(self, f: Callable[[A], bool]) -> Option[A]:
        """Returns the first value that satisfy the predicate"""
        return self.filter(f).head_option()

    def head_option(self) -> Option[A]:
        """Returns the first element, if available"""
        if self.is_empty():
            return Option(None)
        else:
            return Option(self.xs[0])

    def partition(self, f: Callable[[A], bool]) -> Tuple[List[A], List[A]]:
        """
        Partitions the List into two Lists returned as a Tuple. The first List
        contains all elements that satisfy the predicate, the second List contains
        all element that does not satisfy the predicate.
        """
        xs: PList[A] = []
        ys: PList[A] = []
        for x in self.xs:
            if f(x):
                xs.append(x)
            else:
                ys.append(x)

        return List.from_list(xs), List.from_list(ys)

    def nel(self) -> Option[List[A]]:
        """If the List is empty, return an Option.empty else an Option(List[A])"""
        if self.is_empty():
            return Option.empty()
        else:
            return Option(List(self.xs))

    def sorted(self) -> List[A]:
        return List(*sorted(self.xs))

    def reverse(self) -> List[A]:
        return List(*reversed(self.xs))

    def sum(self) -> A:
        return sum(self.xs)

    def length(self) -> int:
        return len(self.xs)

    def unwrap(self):
        """Returns the underlying list"""
        return self.xs

    def diff(self, ys: List[A]) -> List[A]:
        return List(*set(self.xs).difference(ys.unwrap()))

    def append(self, ys: List[A]) -> List[A]:
        return List.from_list(self.xs + ys.unwrap())

    def add(self, x: A) -> List[A]:
        return List.from_list(self.xs + [x])

    def __eq__(self, other) -> bool:
        if isinstance(other, List):
            return self.xs == other.xs
        else:
            return False

    def __repr__(self):
        return f"List({self.mk_string(', ')})"
