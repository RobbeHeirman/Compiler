"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from abc import ABC

import Attributes
import Nodes.AbstractNodes.AbstractNode as AbstractNode
import SymbolTable


class ScopedNode(AbstractNode.AbstractNode, ABC):
    """
    This node is an abstract node that presents all nodes with their own scope.
    This means this node has it's own SymbolTable
    """
    _llvm_register_index: int

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node=None, ctx=None):
        """
        Initializer
        """
        super().__init__(parent_node, ctx)
        self._symbol_table = SymbolTable.SymbolTable()

        self._while_index = 0

    # Semantic analysis
    # ==================================================================================================================
    def add_to_scope_symbol_table(self, lexeme: str, attribute: Attributes.Attributes) -> bool:
        """
        This is a ScopedNode with own symbolTable. We will attempt to add to the symbol table here.
        :param lexeme: The lexeme (id name) of the variable we add
        :param attribute: set of attributes that describes the lexeme
        :return: boolean, true if successfully added, false if not.
        """
        return self._symbol_table.add_id(lexeme, attribute)

    def is_in_table(self, lexeme: str) -> bool:
        """
        Checks if a lexeme is already in the symbol table
        :param lexeme: The lexeme that needs to be returned
        :return: bool if successful = true else false
        """
        if self._symbol_table.is_in_symbol_table(lexeme):
            return True

        else:
            return self._parent_node.is_in_table(lexeme)

    def get_attribute(self, lexeme):
        if self._symbol_table.is_in_symbol_table(lexeme):  # Is declared in this scope.
            return self._symbol_table.get_attribute(lexeme)

        else:
            return self._parent_node.get_attribute(lexeme)  # Looking in higher scoped symbol tables.

    # LLVM Code-Generation
    # ==================================================================================================================
    def is_in_global_table(self, lexeme: str) -> bool:
        """
        Checks if this is in the global table Used for LLVM Code
        :param lexeme: lexeme to check
        :return: bool True if in global table False if not
        """

        if self._symbol_table.is_in_symbol_table(lexeme):
            return False

        return self._parent_node.is_in_global_table(lexeme)

    def is_global(self) -> bool:
        """
        Nodes can ask their parent's if they are global.
        If they are part of a scopedNode they are not.
        :return: A bool False meaning this is not global.
        """
        return False

    def llvm_count_declared_scopes(self, id) -> int:

        if self._symbol_table.is_in_symbol_table(id):
            return self._parent_node.llvm_count_declared_scopes(id) + 1
        return self._parent_node.llvm_count_declared_scopes(id)

    def llvm_found_in_n_scope(self, id, found_first=False) -> int:
        if self._symbol_table.is_in_symbol_table(id):
            if not found_first:
                return self._parent_node.llvm_found_in_n_scope(id, True)

            return 1 + self._parent_node.llvm_found_in_n_scope(id, False)

        return self._parent_node.llvm_found_in_n_scope(id, found_first)

    # Mips-Code
    # ==================================================================================================================
    # Meta Code Generation
    # ==================================================================================================================
    def get_while_label(self):

        func_l = self.code_function_base_label
        ret = f'while_{func_l}{self._while_index}'
        self._while_index += 1
        return ret
