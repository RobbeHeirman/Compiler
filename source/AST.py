"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from source.Nodes.RootNode import RootNode


class AST:
    """Representation of the Abstract syntax tree"""
    _root: RootNode

    def __init__(self):
        """
        Initializer
        """
        self._root = None

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, root):
        self._root = root

    def to_dot(self, filename):
        """
        Generates a string, in dot language format. That can be used as a visual representation for the AST.
        :return:
        """
        graph_string = "graph{\n"
        graph_string += self._root.dot_string()
        graph_string += "}\n"
        file = open(filename, 'w')
        file.write(graph_string)
        file.close()
