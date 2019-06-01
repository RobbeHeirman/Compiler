"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from enum import Enum, auto


class TypeSpecifier(Enum):
    """
    TypeSpecifier Attribute as Enum.
    Specifies a type for a identifier token.
    """
    CHAR = 'char'
    INT = 'int'
    FLOAT = 'float'
    DEFAULT = ''  # Stub when dealing with incomplete info
    ANY = auto()  # Used for type stack printf() scanf()

    @property
    def llvm_type(self) -> str:
        _LLVM_TYPE = {
            self.CHAR: 'i8',
            self.INT: 'i32',
            self.FLOAT: 'float',
            self.DEFAULT: ''
        }

        return _LLVM_TYPE[self]

    @property
    def llvm_alignment(self) -> int:
        _LLVM_ALIGN = {
            self.CHAR: 1,
            self.INT: 4,
            self.FLOAT: 4
        }
        return _LLVM_ALIGN[self]


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


class DeclaratorSpecifier(Enum):
    PTR = "*"
    ARRAY = "[]"
    FUNC = "()"
    ADDRESS = "&"
