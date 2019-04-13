"""
 Author: Robbe Heirman
 Project: Simple C Compiler
 Course: Compilers
 Academic Year: 2018-2019
"""
from source.AST import AST
from source.Nodes.DeclaratorNode import DeclaratorNode
from source.Nodes.ExpressionNode import ExpressionNode
from source.Nodes.BaseTypeNode import BaseTypeNode
from source.Nodes.DeclarationNode import DeclarationNode
from source.Nodes.RootNode import RootNode
from source.Specifiers import TypeSpecifier
from source.gen.CListener import CListener
from source.gen.CParser import CParser


class CListenerExtend(CListener):
    """
    Extension the Generated Antlr CListener.
    Responsible for building the AST
    """
    _filename: str
    _ast: AST
    _parent_node: ExpressionNode

    def __init__(self, filename: str):
        # Some info about the traversing will be recorded

        self._parent_node = None  # Will always keep track of the parent AST node when traversing down
        self._ast = AST()
        self._filename = filename

    @property
    def ast(self):
        return self._ast

    def enterStatements(self, ctx: CParser.StatementContext):
        """
        This is the root of our C program. It will make a root node
        :param ctx: Context of the node
        """
        root_node = RootNode()
        self._ast.root = root_node
        self._parent_node = root_node

    def enterDeclaration(self, ctx: CParser.DeclarationContext):
        """
        Handles a declaration statement. Creates a declaration node. Set it as last parent node so that children can
        can identify their parent
        :param ctx: context of the node
        """

        declaration_node = DeclarationNode(self._parent_node)
        self._parent_node.add_child(declaration_node)
        self._parent_node = declaration_node

    def exitDeclaration(self, ctx: CParser.DeclarationContext):
        """
        Finishes a declaration statement. The node can be resolved. This will mostly attempt to add lexemes
        to the scope's symbol table.
        :param ctx: context of the node
        :return:
        """
        self._parent_node.resolve_expression()
        self._parent_node = self._parent_node.parent_node

    def enterBase_type(self, ctx: CParser.Base_typeContext):
        """
        Leaf of base_type, adds base_type leaf to parent node.
        :param ctx:
        :return:
        """
        start = ctx.start
        line = start.line
        column = start.column
        node = BaseTypeNode(self._parent_node, TypeSpecifier(ctx.getText()), self._filename, line, column)
        self._parent_node.add_child(node)

    def enterDeclarator(self, ctx: CParser.DeclaratorContext):
        """
        Declarator leaf. Enters a declarator leaf to the AST tree.
        :param ctx:
        :return:
        """
        start = ctx.start
        line = start.line
        column = start.column

        node = DeclaratorNode(self._parent_node, ctx.getText(), self._filename, line, column)
        self._parent_node.add_child(node)
