"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""


class TypeSpecifier:
    """
    Will represent a type on the type stack.
    """

    INT = 'int'
    CHAR = 'char'
    FLOAT = 'float'

    POINTER = '*'
    ADDRESS = '&'
    FUNCTION = '()'
    ARRAY = '[]'

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

        if isinstance(o, TypeSpecifier):
            if self._type_spec == o.value:
                return True

        elif isinstance(o, str):
            if self._type_spec == o:
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
        }

        return _LLVM_TYPE.get(self.value, '')
