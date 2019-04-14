"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from abc import ABC, abstractmethod
from typing import List

from source.Nodes import ExpressionNode


class AbstractNode(ABC):
    """
    Abstract class of a node of the AST.
    Should be overridden by specific nodes of the AST.
    """
    _parent_node: ExpressionNode
    _index_counter = 0

    def __init__(self, parent: "AbstractNode" = None):
        """
        Initializer
        """


        # Block for graphviz dot representation.
        self._index = AbstractNode._index_counter
        AbstractNode._index_counter += 1

        self._parent_node = parent

    @property
    def index(self):
        return self._index

    @property
    @abstractmethod
    def label(self):  # Enforcing every node defines a label
        pass

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def parent_node(self) -> "AbstractNode":
        return self._parent_node

    @parent_node.setter
    def parent_node(self, value: "AbstractNode"):
        self._parent_node = value

    def dot_string(self):
        ret = "{0}[label = {1}];\n".format(self._index, self.label)
        return ret

    @property
    def failed(self):
        return False

    @abstractmethod
    def generate_llvm(self):
        pass
