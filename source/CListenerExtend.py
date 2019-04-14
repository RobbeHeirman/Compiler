"""
 Author: Robbe Heirman
 Project: Simple C Compiler
 Course: Compilers
 Academic Year: 2018-2019
"""
from source.AST import AST
from source.Nodes.AssignmentNode import AssignmentNode
from source.Nodes.ConstantNode import ConstantNode
from source.Nodes.DeclaratorNode import DeclaratorNode
from source.Nodes.ExpressionNode import ExpressionNode
from source.Nodes.BaseTypeNode import BaseTypeNode
from source.Nodes.DeclarationNode import DeclarationNode
from source.Nodes.RootNode import RootNode
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

    def enterSimple_declaration(self, ctx: CParser.Simple_declarationContext):
        """
        Handles a declaration statement. Creates a declaration node. Set it as last parent node so that children can
        can identify their parent
        :param ctx: context of the node
        """
        declaration_node = DeclarationNode(self._parent_node)
        self._parent_node.add_child(declaration_node)
        self._parent_node = declaration_node

    def exitSimple_declaration(self, ctx: CParser.Simple_declarationContext):
        """
        Finishes a declaration statement. The node can be resolved. This will mostly attempt to add lexemes
        to the scope's symbol table.
        :param ctx: context of the node
        :return:
        """

        self._parent_node = self._parent_node.parent_node

    def enterBase_type(self, ctx: CParser.Base_typeContext):
        """
        Leaf of base_type, adds base_type leaf to parent node.
        :param ctx:
        :return:
        """

        node = BaseTypeNode(self._parent_node, self._filename, ctx)
        self._parent_node.add_child(node)

    def enterDeclarator(self, ctx: CParser.DeclaratorContext):
        """
        Declarator leaf. Enters a declarator leaf to the AST tree.
        :param ctx:
        :return:
        """

        # column = start.column
        node = DeclaratorNode(self._parent_node, self._filename, ctx)
        self._parent_node.add_child(node)

    def enterAssignment(self, ctx: CParser.AssignmentContext):
        """
        Handle's assignment statement's. We enter the assignment statement so we just make the node.
        :param ctx: ParserContextNode
        :return:
        """

        assignment_node = AssignmentNode(self._parent_node)
        self._parent_node.add_child(assignment_node)
        self._parent_node = assignment_node

    def exitAssignment(self, ctx: CParser.AssignmentContext):
        """
        Finishes the assignment. Expressions RHS & LHS have been evaluated. Now we just need to
        assign the value.
        :param ctx:
        :return:
        """
        self._parent_node = self._parent_node.parent_node

    def enterConstant(self, ctx:CParser.ConstantContext):

        c_node = ConstantNode(self._parent_node,self._filename, ctx)
        self._parent_node.add_child(c_node)
