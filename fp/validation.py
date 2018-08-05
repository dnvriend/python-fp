from __future__ import annotations

from typing import TypeVar, Generic, Callable, Union, Optional

from fp.list import List
from fp.option import Option

A = TypeVar('A')
Err = TypeVar('Err')
C = TypeVar('C')


class Validation(Generic[Err, A]):
    failure: bool = False
    err_value: Err = None
    value: A = None

    @classmethod
    def from_option(cls, opt: Option[A], err: Err) -> Validation[Err, A]:
        if opt.is_defined():
            return Validation.success(opt.get())
        else:
            return Validation.failure(err)

    @classmethod
    def from_optional(cls, opt: Optional[A], err: Err) -> Validation[Err, A]:
        if opt:
            return Validation.success(opt)
        else:
            return Validation.failure(err)

    @classmethod
    def from_try_catch(cls, f: Callable[[], A]) -> Validation[Err, A]:
        try:
            return Validation.success(f())
        except Exception as err:
            return Validation.failure(err)

    @classmethod
    def success(cls, x: A) -> Validation[Err, A]:
        return Success(x)

    @classmethod
    def failure(cls, err: [Err]) -> Validation[Err, A]:
        return Failure(err)

    @classmethod
    def sequence(cls, xs: List[Validation]) -> Validation[List[Err], List[A]]:
        """
        Evaluate each action in the sequence from left to right, and collect the results
        effectively converting F[G[A]] into an G[F[A]].
        """
        err, succ = xs.partition(lambda x: x.is_failure())
        if err.is_empty():
            xs = succ.map(lambda x: x.get())
            return Validation.success(xs)
        else:
            xs = err.map(lambda x: x.get())
            return Validation.failure(xs)

    def map(self, f: Callable[[A], C]) -> Validation[C]:
        if self.is_failure():
            return self
        else:
            return Validation.success(f(self.value))

    def bind(self, f: Callable[[A], Validation[C]]) -> Validation[C]:
        if self.is_failure():
            return self
        else:
            return f(self.value)

    def is_failure(self) -> bool:
        """Returns true if the Validation is an Failure"""
        return self.failure

    def is_success(self) -> bool:
        """Returns true if the Validation is a Success"""
        return not self.failure

    def fold(self, f: Callable[[Err], C], g: Callable[[A], C]) -> C:
        if self.is_failure():
            return f(self.err_value)
        else:
            return g(self.value)

    def get(self) -> Union[Err, A]:
        if self.is_failure():
            return self.err_value
        else:
            return self.value


class Success(Validation):

    def __init__(self, x: A):
        self.failure = False
        self.success = True
        self.value = x

    def __str__(self):
        return f"Success({self.value})"


class Failure(Validation):

    def __init__(self, x: Err):
        self.failure = True
        self.success = False
        self.err_value = x

    def __str__(self):
        return f"Failure({self.err_value})"
