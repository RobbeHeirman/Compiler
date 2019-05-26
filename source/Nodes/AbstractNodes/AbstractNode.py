"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from abc import ABC, abstractmethod
from typing import List

from Nodes.AbstractNodes import NonLeafNode
from SymbolTable import Attributes


class AbstractNode(ABC):
    """
    Abstract class of a node of the AST.
    Should be overridden by specific nodes of the AST.
    """
    _children: List["AbstractNode"]
    _parent_node: NonLeafNode
    _index_counter = 0

    def __init__(self, parent: "AbstractNode" = None):
        """
        Initializer
        """

        # Block for graphviz dot representation.
        self._index = AbstractNode._index_counter
        AbstractNode._index_counter += 1
        self._failed = False
        self._parent_node = parent
        self._children = list()

    @property
    def index(self):
        return self._index

    @property
    @abstractmethod
    def label(self):  # Enforcing every node defines a label
        pass

    @property
    def parent_node(self) -> "AbstractNode":
        return self._parent_node

    @parent_node.setter
    def parent_node(self, value: "AbstractNode"):
        self._parent_node = value

    def dot_string(self):
        ret = "{0}[label = \"{1}\"];\n".format(self._index, self.label)
        return ret

    @abstractmethod
    def generate_llvm(self):
        return ""

    @property
    def failed(self) -> bool:
        for child in self._children:
            self._fail_switch(child.failed)
        return self._failed

    def _fail_switch(self, boolean: bool):
        """
        used so that a node can tell parents there is a semantic error
        :param boolean: the boolean that tells if the expression failed.
        :return:
        """
        if boolean:
            self._failed = True

    def add_to_scope_symbol_table(self, lexeme: str, attribute: Attributes) -> bool:
        """
        Hook to add a lexeme to symbol table. Child classes may need to implement this.
        We will just call the parents add symbol to scope. Scoped nodes contain SymbolTables and will look
        in their own table.
        :param lexeme: the lexeme we want to add.
        :param attribute Attribute object that describes the attributes of the lexeme.
        :return bool true if successfully added, false if not.
        """
        return self._parent_node.add_to_scope_symbol_table(lexeme, attribute)

    @property
    def register_index(self) -> int:
        return self._parent_node.register_index

    def increment_register_index(self):
        self._parent_node.increment_register_index()

    def get_attribute(self, lexeme) -> Attributes:
        return self._parent_node.get_attribute(lexeme)

    def first_pass(self):
        for child in self._children:
            child.first_pass()
