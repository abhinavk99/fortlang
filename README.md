# fortlang

Fortlang - an esoteric programming language based on terms from Fortnite

## Installation
```bash
$ git clone https://github.com/abhinavk99/fortlang.git
```

## Usage
```bash
# Make sure you're in the fortlang directory
$ python fortlang.py
$ input> 3 join 2 leave 4 join 5 leave 3
$ 3
$ input> 9 split 3 group 4 split 3
$ 4.0
# Below statements not supported - the interpreter will exit when seeing the unsupported operation
$ input> 4 leave 1 group 3
# Becomes 4 leave 1 because interpreter exits when it sees 'group'
$ 3
$ input> 12 split 4 join 2
# Becomes 12 split 4 because interpreter exits when it sees 'join'
$ 3.0
```

## Features

Currently, the language is just a CLI interpreter that supports arithmetic expressions
with addition and subtraction and expressions with multiplication and division.
Support between add, subtract and multiply, divide is not supported yet.

## Syntax
* add is `join`
* subtract is `leave`
* multiply is `group`
* divide is `split`

## Todo
I plan on adding the features to make Fortlang an actual language instead of just a simple calculator.
