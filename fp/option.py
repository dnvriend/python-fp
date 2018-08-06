from __future__ import annotations

from typing import TypeVar, Callable, Optional, Generic

A = TypeVar('A')
B = TypeVar('B')


class Option(Generic[A]):

    def __init__(self, opt: Optional[A]):
        self.opt: Optional[A] = opt

    @classmethod
    def empty(cls) -> Option[A]:
        return Option(None)

    @classmethod
    def some(cls, x: A) -> Option[A]:
        return Option(x)

    def map(self, f: Callable[[A], B]) -> Option[B]:
        if self.is_defined():
            return Option(f(self.opt))
        else:
            return self

    def bind(self, f: Callable[[A], Option[B]]) -> Option[B]:
        if self.is_defined():
            return f(self.opt)
        else:
            return self

    def foreach(self, f: Callable[[A], None]) -> None:
        [f(x) for x in list(self.opt)]
        return None

    def filter(self, f: Callable[[A], bool]) -> Option[A]:
        if f(self.opt):
            return self
        else:
            return Option(None)

    def is_empty(self) -> bool:
        return self.opt is None

    def get_or_else(self, default: A) -> A:
        if self.is_defined():
            return self.opt
        else:
            return default

    def mk_string(self, sep='') -> str:
        """Catamorphism to String"""
        return self.fold('', lambda x: str(self.opt))

    def fold_left(self, zero: A, f: Callable[[A, A], A]) -> A:
        """Catamorphism to A"""
        if self.is_defined():
            return f(zero, self.opt)
        else:
            return zero

    def fold_right(self, zero: A, f: Callable[[A, A], A]) -> A:
        """Catamorphism to A"""
        return self.fold_left(zero, f)

    def fold(self, default: B, f: Callable[[A], B]) -> B:
        """Catamorphism to B"""
        return self.map(f).get_or_else(default)

    def get(self) -> A:
        """Returns the underlying value or throws"""
        if self.is_defined():
            return self.opt
        else:
            raise Exception('Option is not defined')

    def is_defined(self) -> bool:
        """Returns true of the Option contains a value"""
        return self.opt is not None

    def __str__(self):
        return f'Option({self.opt})'
