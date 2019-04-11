"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from abc import ABC
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
        """
        self._children = list()
        self._index = AbstractNode._index_counter
        AbstractNode._index_counter += 1

    @property
    def index(self):
        return self._index

    def add_child(self, child: "AbstractNode"):
        """
        Add a child node to the AST.
        :param child: a ASTNode that functions as a child
        """

    def dot_string(self):
        ret = "{0}--{{".format(self._index)
        for child in self._children:
            ret += "{0},".format(child.index)

        ret += "}\n"

        for child in self._children:
            ret += child.dot_string()

        return ret
