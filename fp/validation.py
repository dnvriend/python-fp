from __future__ import annotations

from typing import TypeVar, Generic, Callable, Union, Optional
from dataclasses import dataclass
from fp.list import List

A = TypeVar('A')
Err = TypeVar('Err')
C = TypeVar('C')


@dataclass
class Validation(Generic[Err, A]):

    @classmethod
    def parse_int(cls, s: str) -> Validation[Err, int]:
        return Validation.from_try_catch(lambda: int(s))

    @classmethod
    def parse_float(cls, s: str) -> Validation[Err, float]:
        return Validation.from_try_catch(lambda: float(s))

    @classmethod
    def parse_boolean(cls, s: str):
        return Validation.from_try_catch(lambda: bool(s))

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
    def lift(cls, a: A, f: Callable[[A], bool],
             fail: Err) -> Validation[Err, A]:
        """If True then fail, else succeed"""
        if f(a):
            return Validation.failure(fail)
        else:
            return Validation.success(a)

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
        print(f"is_failure: {self.failure}")
        return self.failure

    def is_success(self) -> bool:
        """Returns true if the Validation is a Success"""
        print(f"is_success: {self.success}")
        return not self.failure

    def fold(self, f: Callable[[Err], C], g: Callable[[A], C]) -> C:
        if self.is_failure():
            print(
                f"fold the error side: failure={self.is_failure()} -> err_value={self.err_value}"
            )
            return f(self.err_value)
        else:
            print(
                f"fold the success side: failure={self.is_failure()} -> value={self.value}"
            )
            return g(self.value)

    def get(self) -> Union[Err, A]:
        if self.is_failure():
            return self.err_value
        else:
            return self.value


@dataclass()
class Success(Validation):
    value: A
    failure: bool = False
    success: bool = True


@dataclass()
class Failure(Validation):
    err_value: Err
    failure: bool = True
    success: bool = False
