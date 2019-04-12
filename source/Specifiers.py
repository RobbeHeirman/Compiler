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
