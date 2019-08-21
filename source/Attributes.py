import typing
import type_specifier


class Attributes:
    """
    Container class used by SymbolTable to keep track of token Attributes
    """
    function_signature: typing.List["Attributes"]

    _base_type: type_specifier.TypeSpecifier
    _operator_stack: typing.List[type_specifier.TypeSpecifier]

    _column: int
    _line: int
    _filename: str

    def __init__(self, type_stack: typing.List[type_specifier.TypeSpecifier], line: int, column: int):
        """
        Initializer
        :param type_stack: The operators applied on the declaration (*, [], ())
        :param line: the line where de lexeme is found.
        :param column: the column where the lexeme is found.
        """

        self._operator_stack = type_stack  # Stacks all the declared operators operators
        self._line = line
        self._column = column

        self.is_const = False

        self.array_size = 0

        # LLVM info
        self._llvm_name = ''

        # Mips info
        self._mips_stack_address: int = 0

    def __eq__(self, val: "Attributes") -> bool:
        if self._operator_stack == val._operator_stack:
            return True
        return False

    @property
    def base_type(self):
        return self._base_type

    @property
    def filename(self) -> str:
        return self._filename

    @filename.setter
    def filename(self, attr):
        self._filename = attr

    @property
    def line(self) -> int:
        return self._line

    @line.setter
    def line(self, val):
        self._line = val

    @property
    def column(self) -> int:
        return self._column

    @column.setter
    def column(self, val):
        self._column = val

    @property
    def decl_type(self):
        return self.base_type

    @property
    def llvm_name(self):
        return self._llvm_name

    @llvm_name.setter
    def llvm_name(self, val):
        self._llvm_name = val

    @property
    def operator_stack(self):
        return list(self._operator_stack)

    # Mips-Code
    # ==================================================================================================================

    @property
    def mips_stack_address(self) -> int:
        return self._mips_stack_address

    @mips_stack_address.setter
    def mips_stack_address(self, val: int):
        self._mips_stack_address = val


class AttributesGlobal(Attributes):
    """
    An extension on attributes for the global table
    """

    def __init__(self, type_stack: typing.List[type_specifier.TypeSpecifier],
                 line: int, column: int, defined: bool, original_declaration_node):
        super().__init__(type_stack, line, column)

        self.function_signature = []
        self.defined = defined

        self.original_declaration_node = original_declaration_node

    def __eq__(self, o):
        if super().__eq__(o):
            if self.function_signature == o.function_signature:
                return True
        return False
