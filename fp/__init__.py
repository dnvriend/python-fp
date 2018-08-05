from typing import TypeVar

A = TypeVar('A')
B = TypeVar('B')


def identity(a: A) -> B:
    return a
