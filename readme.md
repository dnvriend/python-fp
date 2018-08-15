# python-fp
Python modules for functional programming, influenced by the Scala standard lib and Scalaz

## Introduction
Coming from Scala, having some functional programming constructs can be handy.

## Available Functionality
The following is available:

- List[A]
  - map(f: A -> B) -> List[B]
  - bind(f: A -> List[B]) -> List[B]
  - for_each() -> None
  - filter(p: A -> bool) -> List[A]
  - is_empty() -> bool
  - mk_string(sep: str) -> str
  - intersperse(x: A) -> List[A]
  - fold_left(zero: A, f: A, A -> A) -> A
  - fold_right(zero: A, f: A, A -> A) -> A
  - fold(zero: B, B, A -> B): B
  - find(p: A -> bool): Option[A]
  - head_option(): Option[A]
  - partition(f: A -> bool): Tuple[List[A], List[A]]
  - sorted(): List[A]
  - reverse(): List[A]
  - sum(): A
  - length(): int
  - unwrap(): list
- Option[A]
  - map(f: A -> B) -> Option[B]
  - bind(f: A -> Option[B]) -> Option[B]
  - for_each() -> None
  - filter(p: A -> bool) -> List[A]
  - is_empty() -> bool
  - get_or_else(x: A) -> A
  - fold_left(zero: A, f: A, A -> A) -> A
  - fold_right(zero: A, f: A, A -> A) -> A
  - fold(zero: B, f: A -> B): B
  - get(): A
  - is_defined() -> bool  
- Validation[Err, A]
  - sequence(xs: List[Validation]) -> Validation[List[Err], List[A]]
  - from_option(x: Option[A], err: Err): Validation[Err, A]
  - map(f: A, C) -> Validation[C]
  - bind(f: A -> Validation[C]) -> Validation[C]
  - is_failure() -> boolean
  - fold(f: Err -> C, g: Err -> C) -> C
  - get(): Union[Err, A]

## How to build/run
Use the Makefile:

```
$ make
env                            creates a virtual python environment  for this project
info                           shows current python environment
clobber                        remove virtual python environment
fmt                            runs code formatter
type_check                     type checks the code
lint                           run python code analysis on rules
lint_test                      run python code analysis on test


# for example
$ make run
$ make test
$ make fmt
$ make info
```

## Upload to PyPI test
To upload to test PyPI

```bash
# upload to test PyPI
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# install from test PyPI
pip install -i https://testpypi.python.org/pypi python-fp
```

## Upload to PyPI
To upload to PyPI

```bash
# install to PyPI
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

# install from PyPI
pip install python-fp 
```

## Resources
- [Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/)


Have fun!