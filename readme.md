# python-fp
Python modules for functional programming, influenced by the Scala standard lib and Scalaz

## Introduction
Coming from Scala, having some functional programming constructs can be handy.

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

Have fun!