"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from source.Nodes.AbstractNode import AbstractNode


class DeclarationNode(AbstractNode):
    """
    Represents a Declaration in our abstract syntax tree.
    """
    _label = "Declaration"

    def __init__(self):
        super().__init__()


