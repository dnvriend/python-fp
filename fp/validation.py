from __future__ import annotations

from typing import TypeVar, Generic, Callable, List as PList, Optional, Tuple
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
            return Success(opt.get())
        else:
            return Failure(err)

    def is_failure(self) -> bool:
        return self.failure

    def fold(self, err: Callable[[Err], C], success: Callable[[A], C]) -> C:
        if self.is_failure():
            return err(self.err_value)
        else:
            return success(self.value)


class Success(Validation):

    def __init__(self, x: A):
        self.failure = False
        self.success = True
        self.value = x


class Failure(Validation):

    def __init__(self, x: Err):
        self.failure = True
        self.success = False
        self.err_value = x
