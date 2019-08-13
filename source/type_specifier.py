"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import typing


class TypeSpecifier:
    """
    Will represent a type on the type stack.
    """

    INT = 'int'
    CHAR = 'char'
    FLOAT = 'float'
    BOOL = 'bool'

    POINTER = '*'
    ADDRESS = '&'
    FUNCTION = '()'
    ARRAY = '[]'

    ANY = 0  # Needed for printf and scanf

    def __init__(self, type_val: str, func_signature=None):
        """

        :param self:
        :param type_val: a string that represents the type needed, [int, float, chat, *, ()] is the set
        :param func_signature: The function signature
        :return:
        """

        self._type_spec = type_val
        self._function_signature = func_signature if func_signature else []

    def __eq__(self, o):
        val = None
        if isinstance(o, TypeSpecifier):
            val = o.value
        else:
            val = o

        if self._type_spec == val:
            return True

        return False

    def __repr__(self):

        if not self._type_spec == self.__class__.FUNCTION:
            return f'type: {self._type_spec}'

        return f'type: ({self._function_signature})'

    @property
    def value(self):
        return self._type_spec

    @property
    def function_signature(self):
        return self._function_signature

    @function_signature.setter
    def function_signature(self, val):
        self._function_signature = val

    @property
    def llvm_type(self) -> str:
        _LLVM_TYPE = {
            'char': 'i8',
            'int': 'i32',
            'float': 'float',
            '*': '*'
        }

        return _LLVM_TYPE.get(self.value, '')

    @property
    def mips_stack_size(self) -> int:
        """
        Size the value will take on the stack.
        :return int: the size of the stack
        """

        _MIPS_SIZES = {
            "char": 4,  # Actually this is 1 but addressing in 4 contigious bytes
            "int": 4,
            "float": 4,
            "*": 4,
            '[]': 4
        }
        return _MIPS_SIZES[self._type_spec]


# Type aliasing
TypeStack = typing.List[TypeSpecifier]
