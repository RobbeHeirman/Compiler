"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

import Nodes.AbstractNodes.ScopedNode as ScopedNode
import SymbolTable


class RootNode(ScopedNode.ScopedNode):
    """
    The root of our program. Root is a ScopedNode, the base scope of our C program.
    """
    label = "Root"
    _index_counter = 0
    _indent_level = 0

    # Built-ins
    # ==================================================================================================================
    def __init__(self, ctx):
        super().__init__(None, ctx)

        self._symbol_table = SymbolTable.GlobalSymbolTable()

        self._index_counter: int = 0
        self._indent_level: int = 0

        self._index = 0

    # Ast-visuals
    # ==================================================================================================================
    def assign_index(self):
        self._index_counter += 1
        return self._index_counter

    # Semantic analysis
    # ==================================================================================================================
    def is_in_table(self, lexeme: str) -> bool:
        """
        Checks if a lexeme is already in the symbol table
        :param lexeme: The lexeme that needs to be returned
        :return: bool if successful = true else false
        """

        return self._symbol_table.is_in_symbol_table(lexeme)

    def is_in_global_table(self, lexeme: str):
        return self.is_in_table(lexeme)

    def get_attribute(self, lexeme):
        return self._symbol_table.get_attribute(lexeme)

    def is_global(self):
        return True

    # LLVM Code
    # ==================================================================================================================

    def increase_code_indent(self):
        self._indent_level += 1

    def decrease_code_indent(self):
        self._indent_level -= 1

    @property
    def code_indent_level(self):
        return self._indent_level

    # Mips Code
    # ==================================================================================================================

    def generate_mips(self, c_comment: bool = True):
        # We always start by calling main
        ret = "jal main\n"

        # Now we cleanly exit We will return the return of main as exit code
        # Load 17 in to v0 10 = exit (end of program)
        ret += "move $v0 $a0 # We move the return value of main for syscall\n"
        ret += "li $v0, 17 # System call code for end of program\n"
        ret += "syscall\n"

        ret += super().generate_mips()
        return ret
