from __future__ import annotations

from typing import TypeVar

from fp.validation import Validation

Err = TypeVar('Err')


def parse_int(s: str) -> Validation[Err, int]:
    return Validation.from_try_catch(lambda: int(s))


def parse_float(s: str) -> Validation[Err, float]:
    return Validation.from_try_catch(lambda: float(s))


def parse_boolean(s: str):
    return Validation.from_try_catch(lambda: bool(s))
