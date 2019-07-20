"""
 Author: Robbe Heirman
 Project: Simple C Compiler
 Course: Compilers
 Academic Year: 2018-2019
"""
from typing import Union

import AST
import Nodes.AbstractNodes.AbstractNode as AbstractNode
import Nodes.ConditionalNodes.ConditionNode as ConditionNode
import Nodes.ConditionalNodes.IfElseNode as IfElseNode
import Nodes.DeclarationNodes.IncludeStatementNode as IncludeStatementNode
import Nodes.DeclarationNodes.ArrayInitNode as ArrayInitNode
import Nodes.ExpressionNodes.AssignmentNode as AssignmentNode
import Nodes.ExpressionNodes.ConstantExpressionNode as ConstantExpressionNode
import Nodes.DeclarationNodes.DeclListNode as DeclListNode
import Nodes.DeclarationNodes.TypeModifierNode as TypeModifierNode
import Nodes.DeclarationNodes.DeclarationNode as DeclarationNode
import Nodes.ExpressionNodes.IdentifierExpressionNode as IdentifierExpressionNode
import Nodes.ExpressionNodes.LHSNode as LhsNode
import Nodes.FunctionNodes.FuncDefNode as FuncDefNode
import Nodes.FunctionNodes.ParamListNode as ParamListNode
import Nodes.FunctionNodes.ReturnNode as ReturnNode
import Nodes.GlobalNodes.RootNode as RootNode
import Nodes.GlobalNodes.GlobalDeclarationNode as GlobalDeclarationNode
import Nodes.GlobalNodes.StatementsNode as StatementNode
import Specifiers
import type_specifier
import Nodes.AbstractNodes.TypedNode as TypedNode
import Nodes.ExpressionNodes.ExpressionTypeModifierNode as ExpressionTypeModifierNode

from gen.CListener import CListener
from gen.CParser import CParser


class CListenerExtend(CListener):
    """
    Extension the Generated Antlr CListener.
    Responsible for building the AST
    """
    _filename: str
    _ast: AST.AST
    _parent_node: AbstractNode.AbstractNode

    def __init__(self, filename: str, string_stream=None):
        # Some info about the traversing will be recorded

        self._ast = AST.AST(filename, string_stream)
        self._ast.root = RootNode.RootNode()
        self._parent_node = self._ast.root

        # Will help us determine if we are in the global scope.
        self._scope_counter = 0

        # Function def helper
        self._func_def_node = None
        self._prev_node = None

    @property
    def ast(self):
        return self._ast

    def enterStatements(self, ctx: CParser.StatementContext):
        """
        This is the root of our C program. It will make a root node
        :param ctx: Context of the node
        """

        self._scope_counter += 1
        node = StatementNode.StatementsNode(self._parent_node, ctx)
        self._parent_node.add_child(node)
        self._parent_node = node

    def exitStatements(self, ctx: CParser.StatementsContext):

        self._scope_counter -= 1
        self._parent_node = self._parent_node.parent_node

    def enterFunc_def(self, ctx: CParser.Func_defContext):
        func_node = FuncDefNode.FuncDefNode(self._parent_node, ctx)
        self._parent_node.add_child(func_node)
        self._parent_node = func_node
        self._func_def_node = func_node

    def exitFunc_def(self, ctx: CParser.Func_defContext):
        self._parent_node = self._parent_node.parent_node
        self._func_def_node = None

    def enterFunc_declarator(self, ctx: CParser.Func_declaratorContext):
        # noinspection PyTypeChecker
        self.enterDeclarator(ctx)

    def exitFunc_declarator(self, ctx: CParser.Func_declaratorContext):

        # noinspection PyTypeChecker
        self.exitDeclarator(ctx)

    def enterParameter_list(self, ctx: CParser.Parameter_listContext):
        node = ParamListNode.ParamListNode(self._parent_node)
        self._parent_node.add_child(node)
        self._parent_node = node

    def exitParameter_list(self, ctx: CParser.Parameter_listContext):
        self._parent_node = self._parent_node.parent_node

    def enterRet_statement(self, ctx: CParser.Ret_statementContext):

        ret_node = ReturnNode.ReturnNode(self._parent_node, ctx)
        self._parent_node.add_child(ret_node)
        self._parent_node = ret_node

    def exitRet_statement(self, ctx: CParser.Ret_statementContext):
        self._parent_node = self._parent_node.parent_node

    def enterParam(self, ctx: CParser.ParamContext):
        decl_node = DeclarationNode.DeclarationNode(self._parent_node, ctx)
        self._parent_node.add_child(decl_node)
        self._parent_node = decl_node

    def exitParam(self, ctx: CParser.ParamContext):
        self._parent_node = self._parent_node.parent_node

    # Simple Declarations
    # ======================================================================================================================
    def enterDecl_list(self, ctx: CParser.Decl_listContext):
        """
        Entering decl list example : int, a, b = 10, c..;
        :param ctx:
        :return:
        """
        decl_l_node = DeclListNode.DeclListNode(self._parent_node)
        self._parent_node.add_child(decl_l_node)
        self._parent_node = decl_l_node

    def exitDecl_list(self, ctx: CParser.Decl_listContext):
        self._parent_node.cleanup()
        self._parent_node = self._parent_node.parent_node

    def enterSimple_declaration(self, ctx: CParser.Simple_declarationContext):
        """
        Handles a declaration statement. Creates a declaration node. Set it as last parent node so that children can
        can identify their parent
        :param ctx: context of the node
        """

        declaration_node = GlobalDeclarationNode.GlobalDeclarationNode(self._parent_node, ctx) \
            if self._scope_counter == 0 \
            else DeclarationNode.DeclarationNode(self._parent_node, ctx)

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
        Leaf of base_type, adds base_type to parent node.
        :param ctx:
        :return:
        """
        value = ctx.getText()
        self._parent_node: TypedNode.TypedNode
        self._parent_node.set_base_type(type_specifier.TypeSpecifier(value))

    def enterDeclarator(self, ctx: CParser.DeclaratorContext):
        """
        Declarator leaf. Enters a declarator leaf to the AST tree.
        :param ctx:
        :return:
        """
        # column = start.column
        if ctx.getChild(0).getText() is not "(":  # parenthesis are just used to order
            node = TypeModifierNode.TypeModifierNode(self._parent_node, ctx)
            self._parent_node.add_child(node)
            self._parent_node = node

    def exitDeclarator(self, ctx: CParser.DeclaratorContext):

        if ctx.getChild(0).getText() is not "(":
            self._parent_node = self._parent_node.parent_node

    def enterPtr_decl(self, ctx: CParser.Ptr_declContext):

        self._parent_node.modifier_type = type_specifier.TypeSpecifier.POINTER

    def enterFunction_operator(self, ctx: CParser.Function_operatorContext):

        if self._func_def_node:
            self._prev_node = self._parent_node
            self._parent_node = self._func_def_node
        else:
            self._parent_node.modifier_type = type_specifier.TypeSpecifier.FUNCTION

    def exitFunction_operator(self, ctx: CParser.Function_operatorContext):

        if self._func_def_node:
            self._parent_node = self._prev_node

    def enterArray_operator(self, ctx: CParser.Array_operatorContext):

        self._parent_node.modifier_type = type_specifier.TypeSpecifier.ARRAY

    def enterId_decl(self, ctx: CParser.Id_declContext):
        self._parent_node: Union[DeclarationNode.DeclarationNode, TypeModifierNode.TypeModifierNode]
        self._parent_node.add_id(ctx.getText())
        # Is just a stub. We propagated the identifier. So the node is no necessary.
        self._parent_node.parent_node.remove_child(self._parent_node)

    # Initialize a declaration
    # ======================================================================================================================

    def enterArray_init(self, ctx: CParser.Array_initContext):
        node = ArrayInitNode.ArrayInitNode(self._parent_node)
        self._parent_node.add_child(node)
        self._parent_node = node

    def exitArray_init(self, ctx: CParser.Array_initContext):
        self._parent_node = self._parent_node.parent_node

    def enterAssignment(self, ctx: CParser.AssignmentContext):
        """
        Handle's assignment statement's. We enter the assignment statement so we just make the node.
        :param ctx: ParserContextNode
        :return:
        """
        assignment_node = AssignmentNode.AssignmentNode(self._parent_node, self._filename, ctx)
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

    def enterLhs(self, ctx: CParser.LhsContext):

        node = LhsNode.LHSNode(self._parent_node)
        self._parent_node.add_child(node)
        self._parent_node = node

    def exitLhs(self, ctx: CParser.LhsContext):
        self._parent_node = self._parent_node.parent_node

    # Expressions
    # ======================================================================================================================

    def enterFix_expression(self, ctx: CParser.Fix_expressionContext):
        """
        If on the expression rule a prefix expression is chosen. We create a typeModifierNode.
        This is filled in later by the prefix rule itself.

        """
        prefix_node = ExpressionTypeModifierNode.ExpressionTypeModifierNode(self._parent_node, ctx)
        # The expression Node gets linked on exit (and found as well)
        if isinstance(self._parent_node, TypeModifierNode.TypeModifierNode):
            self._parent_node.add_child(prefix_node)

        prefix_node.parent_node = self._parent_node
        self._parent_node = prefix_node

    def exitFix_expression(self, ctx: CParser.Fix_expressionContext):
        """
        We want to place the prefixes as children of other expressions.
        """

        # We can do this bcz exit is bottom up, and the recursive calls stops at a non type modifier expression.
        expressive_node = self._parent_node.pop_child(0)

        expressive_node.add_child(self._parent_node)  # parent node is the type modifier

        self._parent_node.parent_node.add_child(expressive_node)
        expressive_node.parent_node = self._parent_node.parent_node

        self._parent_node = self._parent_node.parent_node

    def enterConstant(self, ctx: CParser.ConstantContext):
        c_node = ConstantExpressionNode.ConstantExpressionNode(self._parent_node, ctx)
        self._parent_node.add_child(c_node)
        c_node.parent_node = self._parent_node
        self._parent_node = c_node

    def exitConstant(self, ctx: CParser.ConstantContext):
        self._parent_node = self._parent_node.parent_node

    def enterCharacter_constant(self, ctx: CParser.Character_constantContext):
        self._parent_node: ConstantExpressionNode.ConstantExpressionNode
        self._parent_node.set_base_type(type_specifier.TypeSpecifier.CHAR)

    def enterFloating_constant(self, ctx: CParser.Floating_constantContext):
        self._parent_node: ConstantExpressionNode.ConstantExpressionNode
        self._parent_node.set_base_type(type_specifier.TypeSpecifier.FLOAT)

    def enterInteger_constant(self, ctx: CParser.Integer_constantContext):
        self._parent_node: ConstantExpressionNode.ConstantExpressionNode
        self._parent_node.set_base_type(type_specifier.TypeSpecifier.INT)

    def enterId_expression(self, ctx: CParser.Id_expressionContext):
        id_node = IdentifierExpressionNode.IdentifierExpressionNode(self._parent_node, ctx)
        self._parent_node.add_child(id_node)
        self._parent_node = id_node

    def exitId_expression(self, ctx: CParser.Id_expressionContext):
        node = self._parent_node
        self._parent_node = self._parent_node.parent_node
        node.parent_node = self._parent_node

    def enterExpression_prefix(self, ctx: CParser.Expression_prefixContext):
        val = ctx.getChild(0).getText()
        self._parent_node.modifier_type = type_specifier.TypeSpecifier(val)

    def enterExpression_postfix(self, ctx: CParser.Expression_postfixContext):
        val = ctx.getChild(0).getChild(0).getText() + ctx.getChild(0).getChild(2).getText()
        self._parent_node.modifier_type = type_specifier.TypeSpecifier(val)

    def enterExpression_param_list(self, ctx: CParser.Expression_param_listContext):

        node = ParamListNode.ParamListNode(self._parent_node)
        self._parent_node.add_child(node)
        self._parent_node = node

    def exitExpression_param_list(self, ctx: CParser.Expression_param_listContext):
        self._parent_node = self._parent_node.parent_node

    def enterInclude_statement(self, ctx: CParser.Include_statementContext):

        node = IncludeStatementNode.IncludeStatementNode(self._parent_node, self._filename, ctx)
        self._parent_node.add_child(node)
        self._parent_node = node

    def exitInclude_statement(self, ctx: CParser.Include_statementContext):
        self._parent_node = self._parent_node.parent_node

    def enterIf_statement(self, ctx: CParser.If_statementContext):

        c_type = Specifiers.ConditionType.IF
        node = IfElseNode.IfElseNode(self._parent_node, c_type)

        self._parent_node.add_child(node)
        self._parent_node = node

    def exitIf_statement(self, ctx: CParser.If_statementContext):
        self._parent_node = self._parent_node.parent_node

    def enterElse_if_statement(self, ctx: CParser.Else_if_statementContext):
        c_type = Specifiers.ConditionType.ELSE_IF
        node = IfElseNode.IfElseNode(self._parent_node, c_type)

        self._parent_node.add_child(node)
        self._parent_node = node

    def exitElse_if_statement(self, ctx: CParser.Else_if_statementContext):
        self._parent_node = self._parent_node.parent_node

    def enterElse_statement(self, ctx: CParser.Else_statementContext):
        c_type = Specifiers.ConditionType.ELSE
        node = IfElseNode.IfElseNode(self._parent_node, c_type)

        self._parent_node.add_child(node)
        self._parent_node = node

    def exitElse_statement(self, ctx: CParser.Else_statementContext):
        self._parent_node = self._parent_node.parent_node

    def enterWhile_statement(self, ctx: CParser.While_statementContext):

        c_type = Specifiers.ConditionType.WHILE
        node = IfElseNode.IfElseNode(self._parent_node, c_type)
        self._parent_node.add_child(node)
        self._parent_node = node

    def exitWhile_statement(self, ctx: CParser.While_statementContext):
        self._parent_node = self._parent_node.parent_node

    def enterCondition(self, ctx: CParser.ConditionContext):

        op_val = ctx.getChild(1).getText()
        node = ConditionNode.ConditionNode(self._parent_node, op_val)
        self._parent_node.add_child(node)
        self._parent_node = node

    def exitCondition(self, ctx: CParser.ConditionContext):
        self._parent_node = self._parent_node.parent_node
