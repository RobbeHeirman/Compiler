"""
 Author: Robbe Heirman
 Project: Simple C Compiler
 Course: Compilers
 Academic Year: 2018-2019
"""
from source.AST import AST
from source.Nodes.ExpressionNodes.AssignmentNode import AssignmentNode
from source.Nodes.ExpressionNodes.ConstantNode import ConstantNode
from source.Nodes.DeclarationNodes.DeclListNode import DeclListNode
from source.Nodes.DeclarationNodes.DeclaratorNode import DeclaratorNode
from source.Nodes.AbstractNodes.ExpressionNode import ExpressionNode
from source.Nodes.DeclarationNodes.BaseTypeNode import BaseTypeNode
from source.Nodes.DeclarationNodes.DeclarationNode import DeclarationNode
from source.Nodes.FunctionNodes.FuncDefNode import FuncDefNode
from source.Nodes.ExpressionNodes.IdNode import IdNode
from source.Nodes.ExpressionNodes.RHSNode import RHSNode
from source.Nodes.FunctionNodes.ReturnNode import ReturnNode
from source.Nodes.GlobalNodes.RootNode import RootNode
from source.Specifiers import Operator
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
        root_node = RootNode()
        self._ast.root = root_node
        self._parent_node = root_node

    @property
    def ast(self):
        return self._ast

    def enterStatements(self, ctx: CParser.StatementContext):
        """
        This is the root of our C program. It will make a root node
        :param ctx: Context of the node
        """

    def enterFunc_def(self, ctx: CParser.Func_defContext):
        func_node = FuncDefNode(self._parent_node, ctx.getChild(1).getText(), self._filename, ctx.getChild(1))
        self._parent_node.add_child(func_node)
        self._parent_node = func_node

    def exitFunc_def(self, ctx: CParser.Func_defContext):
        self._parent_node = self._parent_node.parent_node

    def enterRet_statement(self, ctx: CParser.Ret_statementContext):

        ret_node = ReturnNode(self._parent_node)
        self._parent_node.add_child(ret_node)
        self._parent_node = ret_node

    def exitRet_statement(self, ctx: CParser.Ret_statementContext):
        self._parent_node = self._parent_node.parent_node

    def enterParam(self, ctx: CParser.ParamContext):
        decl_node = DeclarationNode(self._parent_node)
        self._parent_node.add_child(decl_node)
        self._parent_node = decl_node

    def exitParam(self, ctx: CParser.ParamContext):
        self._parent_node = self._parent_node.parent_node

    def enterDecl_list(self, ctx: CParser.Decl_listContext):
        """
        Entering decl list example : int, a, b = 10, c..;
        :param ctx:
        :return:
        """
        decl_l_node = DeclListNode(self._parent_node)
        self._parent_node.add_child(decl_l_node)
        self._parent_node = decl_l_node

    def exitDecl_list(self, ctx: CParser.Decl_listContext):

        self._parent_node = self._parent_node.parent_node

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
        id_name = ctx.getChild(0).getText()
        assignment_node = AssignmentNode(self._parent_node, id_name, self._filename, ctx)
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

    def enterRhs(self, ctx: CParser.RhsContext):
        """
        Any (sub) expression need to handle the operator kind
        :param ctx:  ParserContextNode
        :return:
        """

        if ctx.getChild(0).getText() == '-':
            node = RHSNode(self._parent_node, negative=True)
            self._parent_node.add_child(node)
            self._parent_node = node

        elif ctx.getChildCount() == 2:
            child = ctx.getChild(1)
            if ctx.getChild(1).getText() == "++" or ctx.getChild(1).getText() == "--":
                operator = Operator(child.getText())
                rhs_node = RHSNode(self._parent_node, operator = operator)
                self._parent_node.add_child(rhs_node)
                self._parent_node = rhs_node
        elif ctx.getChildCount() == 3:  # Looking for the operator token
            child = ctx.getChild(1)
            if child.getChildCount() == 0:  # Ignoring the parentheses, parser forced order of operations.
                operator = Operator(child.getText())
                rhs_node = RHSNode(self._parent_node, operator=operator)
                self._parent_node.add_child(rhs_node)
                self._parent_node = rhs_node

    def exitRhs(self, ctx:CParser.RhsContext):
        """
        Need to pop the rhs nodes from the parent node
        :param ctx:
        :return:
        """

        if ctx.getChild(0).getText() == '-':
            self._parent_node = self._parent_node.parent_node

        elif ctx.getChildCount() == 2:
            if ctx.getChild(1).getText() == "++" or ctx.getChild(1).getText() == "--":
                self._parent_node = self._parent_node.parent_node

        elif ctx.getChildCount() == 3:
            if ctx.getChild(1).getChildCount() == 0:
                self._parent_node = self._parent_node.parent_node

    def enterConstant(self, ctx: CParser.ConstantContext):
        c_node = ConstantNode(self._parent_node, self._filename, ctx)
        self._parent_node.add_child(c_node)

    def enterId_rhs(self, ctx: CParser.Id_rhsContext):
        id_node = IdNode(self._parent_node, self._filename, ctx)
        self._parent_node.add_child(id_node)
