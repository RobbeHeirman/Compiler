"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

from enum import Enum, auto


class Operator(Enum):
    ADD = '+'
    SUB = '-'
    MULT = '*'
    DIV = '/'
    POW = '^'
    REM = '%'
    INCR = '++'
    DECR = '--'
    DEFAULT = ''

    def bin_operator_map(self):
        _BINARY_LLVM_MAPPING = {
            self.ADD: 'add',
            self.SUB: 'sub',
            self.MULT: 'mul',
            self.DIV: 'sdiv',
            self.REM: 'srem'

        }
        return _BINARY_LLVM_MAPPING[self]


class ConditionalOperator(Enum):
    BIGGER = '>'
    SMALLER = '<'
    EQUALS = '=='


class ConditionType(Enum):
    IF = 'if'
    ELSE_IF = 'else if'
    ELSE = 'else'
    WHILE = 'while'
