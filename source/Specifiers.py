"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from enum import Enum


class TypeSpecifier(Enum):
    """
    TypeSpecifier Attribute as Enum.
    Specifies a type for a identifier token.
    """
    CHAR = 'char'
    INT = 'int'
    FLOAT = 'float'
    DEFAULT = ''  # Stub when dealing with incomplete info

    @property
    def llvm_type(self) ->str:
        _LLVM_TYPE = {
            self.CHAR: 'i8',
            self.INT: 'i32',
            self.FLOAT: 'float'
        }

        return _LLVM_TYPE[self]

    @property
    def llvm_alignment(self) ->int:
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
