"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.DeclarationNodes import DeclarationNode


class GlobalDeclarationNode(DeclarationNode.DeclarationNode):
    _BASE_LABEL = "GlobalDeclaration"

    def __init__(self, parent_node, filename, ctx):
        print("CALL MEEE")
        super().__init__(parent_node, filename, ctx)

    # Semantic analysis different,

    # Code gen different
