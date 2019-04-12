"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from abc import ABC, abstractmethod
from typing import List


class AbstractNode(ABC):
    """
    Abstract class of a node of the AST.
    Should be overridden by specific nodes of the AST.
    """
    _children: List["AbstractNode"]
    _index_counter = 0

    def __init__(self):
        """
        Initializer
        Index
        """
        self._children = list()

        # Block for graphviz dot representation.
        self._index = AbstractNode._index_counter
        AbstractNode._index_counter += 1

    @property
    def index(self):
        return self._index

    @property
    @abstractmethod
    def _label(self): # Enforcing every node defines a label
        pass

    def add_child(self, child: "AbstractNode"):
        """
        Add a child node to the AST.
        :param child: a ASTNode that functions as a child
        """

    def dot_string(self):
        """Generates the visual representation of the node in .dot"""
        ret = "{0}[label = {1}];\n".format(self._index, self._label)
        ret += "{0}--{{".format(self._index)
        for child in self._children:
            ret += "{0},".format(child.index)

        ret += "}\n"

        for child in self._children:
            ret += child.dot_string()

        return ret
