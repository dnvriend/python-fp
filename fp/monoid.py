from __future__ import annotations

from typing import TypeVar, Generic

A = TypeVar('A')


class Monoid(Generic[A]):

    def zero(self) -> A:
        pass

    def append(self, l: A, r: A) -> A:
        pass


class StringMonoid(Monoid[str]):

    def zero(self) -> str:
        return ''

    def append(self, l: str, r: str) -> str:
        return l + r

    def __repr__(self) -> str:
        return 'StringMonoid'


class IntMonoid(Monoid[int]):

    def zero(self) -> int:
        return 0

    def append(self, l: int, r: int) -> int:
        return l + r

    def __repr__(self) -> str:
        return 'IntMonoid'
