from typing import TypeVar, Generic

from fp.list import List
from fp.option import Option
from fp.validation import Validation

A = TypeVar('A')
B = TypeVar('B')
Err = TypeVar('Err')


class OptionSequence(Generic[A]):

    @classmethod
    def sequence(cls, xs: List[Option[A]]) -> Option[List[A]]:
        """
        Evaluate each action in the sequence from left to right, and collect the results
        effectively converting F[G[A]] into an G[F[A]].
        """
        _, xs = xs.partition(lambda x: x.is_empty())
        if xs.is_empty():
            return Option.empty()
        else:
            return Option(xs.map(lambda x: x.get()))


class ValidationSequence(Generic[A]):

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
