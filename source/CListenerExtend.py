"""
 Author: Robbe Heirman
 Project: Simple C Compiler
 Course: Compilers
 Academic Year: 2018-2019
"""
from source.AST import AST
from source.Nodes import AbstractNode
from source.Nodes.RootNode import RootNode
from source.gen.CListener import CListener
from source.gen.CParser import CParser


class CListenerExtend(CListener):
    """
    Extension the Generated Antlr CListener.
    Responsible for building the AST
    """
    _parent_node: AbstractNode

    def __init__(self):
        # Some info about the traversing will be recorded

        self._parent_node = None # Will always keep track of the parent AST node when traversing down
        self._ast = AST()

    def enterStatements(self, ctx:CParser.StatementContext):
        """
        This is the root of our C program. It will make a root node
        :param ctx: Context of the node
        """
        root_node = RootNode()
        self._ast.root = root_node
        self._parent_node = root_node

    def enterDeclaration(self, ctx: CParser.DeclarationContext):
        """
        Handles a declaration statement. the identifier needs to be added to the symbol table with corresponding
        attributes. Also handles semantic errors like a redeclaration of an identifier.
        :param ctx: context of the node
        """
        base_type = None
        for i in range(ctx.getChildCount()):
            child = ctx.getChild(i).getPayload()
            print(type(ctx.getChild(i).getPayload()))

            if isinstance(child, CParser.Base_typeContext):
                print("yay!")