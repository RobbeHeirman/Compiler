"""
 Author: Robbe Heirman
 Project: Simple C Compiler
 Course: Compilers
 Academic Year: 2018-2019
"""
from typing import Union

import AST
import Nodes.AbstractNodes.AbstractNode as AbstractNode
import Nodes.ExpressionNodes.ConditionNode as ConditionNode
import Nodes.DeclarationNodes.IncludeStatementNode as IncludeStatementNode
import Nodes.DeclarationNodes.ArrayInitNode as ArrayInitNode
import Nodes.ExpressionNodes.ConstantExpressionNode as ConstantExpressionNode
import Nodes.DeclarationNodes.DeclListNode as DeclListNode
import Nodes.DeclarationNodes.DeclarationTypeModifierNode as TypeModifierNode
import Nodes.DeclarationNodes.DeclarationNode as DeclarationNode
import Nodes.ExpressionNodes.IdentifierExpressionNode as IdentifierExpressionNode
import Nodes.FunctionNodes.FuncDefNode as FuncDefNode
import Nodes.FunctionNodes.ParamListNode as ParamListNode
import Nodes.FunctionNodes.ReturnNode as ReturnNode
import Nodes.GlobalNodes.RootNode as RootNode
import Nodes.GlobalNodes.GlobalDeclarationNode as GlobalDeclarationNode
import Nodes.GlobalNodes.StatementsNode as StatementNode

import type_specifier
import Nodes.AbstractNodes.TypedNode as TypedNode
import Nodes.ExpressionNodes.ExpressionTypeModifierNode as ExpressionTypeModifierNode
from Nodes.ConditionalNodes import BranchNode, IfNode, ElseNode
from Nodes.ConditionalNodes.BreakNode import BreakNode
from Nodes.ConditionalNodes.ElifNode import ElseIfNode
from Nodes.ConditionalNodes.WhileNode import WhileNode
from Nodes.ExpressionNodes import AssignmentNode, BinaryArethmicOperatorNode

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

    # Build-ins
    # ==================================================================================================================
    def __init__(self, filename: str, string_stream=None):
        # Some info about the traversing will be recorded

        self._ast = AST.AST(filename, string_stream)

        # Will help us determine if we are in the global scope.
        self._scope_counter = 0

        # Function def helper
        self._func_def_node = None
        self._prev_node = None

    # Properties
    # ==================================================================================================================
    @property
    def ast(self):
        return self._ast

    # Global Scope
    # ==================================================================================================================
    def enterRoot(self, ctx: CParser.RootContext):
        self._ast.root = RootNode.RootNode(ctx)
        self._parent_node = self._ast.root

    # Local Scope
    # ==================================================================================================================
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

    # Functions
    # ==================================================================================================================
    def enterFunc_def(self, ctx: CParser.Func_defContext):
        func_node = FuncDefNode.FuncDefNode(self._parent_node, ctx)
        self._parent_node.add_child(func_node)
        self._parent_node = func_node
        self._func_def_node = func_node

    def exitFunc_def(self, ctx: CParser.Func_defContext):
        self._parent_node: FuncDefNode.FuncDefNode
        self._parent_node.remove_modifier_node()
        self._parent_node = self._parent_node.parent_node
        self._func_def_node = None

    def enterFunc_declarator(self, ctx: CParser.Func_declaratorContext):
        # noinspection PyTypeChecker
        self.enterNormal_declarator(ctx)

    def exitFunc_declarator(self, ctx: CParser.Func_declaratorContext):

        # noinspection PyTypeChecker
        self.exitNormal_declarator(ctx)

    def enterParameter_list(self, ctx: CParser.Parameter_listContext):
        node = ParamListNode.ParamListNode(self._parent_node, ctx)
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
    # ==================================================================================================================
    def enterDecl_list(self, ctx: CParser.Decl_listContext):
        """
        Entering decl list example : int, a, b = 10, c..;
        :param ctx:
        :return:
        """
        decl_l_node = DeclListNode.DeclListNode(self._parent_node, ctx)
        self._parent_node.add_child(decl_l_node)
        self._parent_node = decl_l_node

    def exitDecl_list(self, ctx: CParser.Decl_listContext):

        self._parent_node.cleanup()
        self._parent_node = self._parent_node.parent_node

    def enterType_qualifier(self, ctx: CParser.Type_qualifierContext):

        self._parent_node: DeclListNode
        self._parent_node.is_const = True

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

    def enterNormal_declarator(self, ctx: CParser.Normal_declaratorContext):
        """
        Declarator leaf. Enters a declarator leaf to the AST tree.
        :param ctx:
        :return:
        """
        # column = start.column

        node = TypeModifierNode.TypeModifierNode(self._parent_node, ctx)
        self._parent_node.add_child(node)
        self._parent_node = node

    def exitNormal_declarator(self, ctx: CParser.DeclaratorContext):

        self._parent_node = self._parent_node.parent_node

        if isinstance(self._parent_node, TypeModifierNode.TypeModifierNode):
            if not self._parent_node.modifier_type:
                raise ValueError("Modifier Types should have their types filled in")

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
            self._func_def_node = None

    def enterArray_operator(self, ctx: CParser.Array_operatorContext):

        self._parent_node.modifier_type = type_specifier.TypeSpecifier.ARRAY

    def enterId_decl(self, ctx: CParser.Id_declContext):
        self._parent_node: Union[DeclarationNode.DeclarationNode, TypeModifierNode.TypeModifierNode]
        self._parent_node.add_id(ctx.getText())
        # Is just a stub. We propagated the identifier. So the node is no necessary.

    # Initialize a declaration
    # ======================================================================================================================

    def enterArray_init(self, ctx: CParser.Array_initContext):
        node = ArrayInitNode.ArrayInitNode(self._parent_node)
        self._parent_node.add_child(node)
        self._parent_node = node

    def exitArray_init(self, ctx: CParser.Array_initContext):
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

        self._parent_node.parent_node.remove_child(self._parent_node)
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
        val = ctx.getChild(0).getChild(0).getText()

        val = '[]' if val == '[' else '()'
        self._parent_node.modifier_type = type_specifier.TypeSpecifier(val)

    def enterExpression_param_list(self, ctx: CParser.Expression_param_listContext):

        node = ParamListNode.ParamListNode(self._parent_node, ctx)
        self._parent_node.add_child(node)
        self._parent_node = node

    def exitExpression_param_list(self, ctx: CParser.Expression_param_listContext):
        self._parent_node = self._parent_node.parent_node

    # Binary Operator's
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Assignment operator
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def enterAssignment_expression(self, ctx: CParser.Assignment_expressionContext):
        """
        Handle's assignment expression's => expr = expr
        :param ctx: The Parser Node we retrieve info from
        """

        assignment_node = AssignmentNode.AssignmentNode(self._parent_node, ctx)
        self._parent_node.add_child(assignment_node)
        self._parent_node = assignment_node

    def exitAssignment_expression(self, ctx: CParser.Assignment_expressionContext):
        self._parent_node = self._parent_node.parent_node

    # Arithmetic operator
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def enterBinary_operator(self, ctx: CParser.Binary_operatorContext):
        bin_node = BinaryArethmicOperatorNode.BinaryArethmicOperatorNode(self._parent_node, ctx)
        self._parent_node.add_child(bin_node)
        self._parent_node = bin_node

    def exitBinary_operator(self, ctx: CParser.Binary_operatorContext):
        self._parent_node = self._parent_node.parent_node

    # Conditional operator
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def enterCondition(self, ctx: CParser.ConditionContext):

        op_val = ctx.getChild(1).getText()
        node = ConditionNode.ConditionNode(self._parent_node, ctx, op_val)
        self._parent_node.add_child(node)
        self._parent_node = node

    def exitCondition(self, ctx: CParser.ConditionContext):
        self._parent_node = self._parent_node.parent_node

    # Includes
    # ==================================================================================================================
    def enterInclude_statement(self, ctx: CParser.Include_statementContext):

        node = IncludeStatementNode.IncludeStatementNode(self._parent_node, ctx)
        self._parent_node.add_child(node)
        self._parent_node = node

    def exitInclude_statement(self, ctx: CParser.Include_statementContext):
        self._parent_node = self._parent_node.parent_node

    # Branching
    # ==================================================================================================================
    def enterBranch(self, ctx: CParser.BranchContext):

        node = BranchNode.BranchNode(self._parent_node, ctx)
        self._parent_node.add_child(node)
        self._parent_node = node

    def exitBranch(self, ctx: CParser.BranchContext):
        self._parent_node = self._parent_node.parent_node

    def enterC_if(self, ctx: CParser.C_ifContext):
        node = IfNode.IfNode(self._parent_node, ctx)
        self._parent_node.add_child(node)
        self._parent_node = node

    def exitC_if(self, ctx: CParser.C_ifContext):
        self._parent_node = self._parent_node.parent_node

    def enterC_elif(self, ctx: CParser.C_elifContext):
        node = ElseIfNode(self._parent_node, ctx)
        self._parent_node.add_child(node)
        self._parent_node = node

    def exitC_elif(self, ctx: CParser.C_elifContext):
        self._parent_node = self._parent_node.parent_node

    def enterC_else(self, ctx: CParser.C_elseContext):
        node = ElseNode.ElseNode(self._parent_node, ctx)
        self._parent_node.add_child(node)
        self._parent_node = node

    def exitC_else(self, ctx: CParser.C_elseContext):
        self._parent_node = self._parent_node.parent_node

    def enterWhile_loop(self, ctx: CParser.While_loopContext):
        node = WhileNode(self._parent_node, ctx)
        node.parent_node = self._parent_node
        self._parent_node.add_child(node)
        self._parent_node = node

    def exitWhile_loop(self, ctx: CParser.While_loopContext):
        self._parent_node = self._parent_node.parent_node

    def enterBreak_statement(self, ctx: CParser.Break_statementContext):
        self._parent_node.add_child(BreakNode(self._parent_node, ctx))
