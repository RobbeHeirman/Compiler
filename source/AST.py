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

        self._root = RootNode()

    def to_dot(self, filename):
        """
        Generates a string, in dot language format. That can be used as a visual representation for the AST.
        :return:
        """

        file = open(filename, 'w')
        file.write(self._root.dot_string())
