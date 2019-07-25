"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

import Nodes.AbstractNodes.TypedNode as TypedNode
import Nodes.DeclarationNodes.ArrayInitNode as ArrayInitNode
import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode

import LlvmCode
import Attributes as Attributes
import messages
from Nodes.AbstractNodes.AbstractNode import AbstractNode
from Nodes.ExpressionNodes.ExpressionTypeModifierNode import ExpressionTypeModifierNode


class DeclarationNode(TypedNode.TypedNode):
    """
    Represents a GlobalDeclaration in our abstract syntax tree.
    Will deduct the base type of the declaration in the first pass.
    Has 1 or 2 children a declarator (will become a stack of pre and postfix type specifiers after first pass)
    An optional initializer as 2d child.
    """

    # Type annotations members

    _lexeme: str

    _BASE_LABEL = "Declaration"

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)

        self.id = None
        self._expression_node = None
        # Error message info

    # AST Visuals
    # ==================================================================================================================
    @property
    def label(self):
        ret_label = self._BASE_LABEL
        if self._type_stack:
            ret_label += f"\\n Type: {[val.value for val in self._type_stack]}"

        if self.id is not None:
            ret_label += f"\\n Identifier: {self.id}"

        return ret_label

    # AST Generation
    # ==================================================================================================================
    def add_id(self, identifier):

        self.id = identifier

    def add_child(self, child, index: int = None):
        """
        extends add_child of abstractNode. To quick filter useful information for DeclarationNode
        :param index: index where to add
        :param child: An abstractNode
        """
        if isinstance(child, ExpressionTypeModifierNode):
            AbstractNode.add_child(self, child)
            return

        if isinstance(child, ExpressionNode.ExpressionNode) or isinstance(child, ArrayInitNode.ArrayInitNode):
            self._expression_node = child

        elif child is None:
            print("happens")

        super().add_child(child)

    def remove_child(self, child: "AbstractNode"):

        if isinstance(child, ExpressionTypeModifierNode):
            AbstractNode.remove_child(self, child)
        else:
            super().remove_child(child)
            return

    # Semantic analysis
    # ==================================================================================================================
    def semantic_analysis(self, messenger: messages.MessageGenerator) -> bool:
        """
        On a declaration, a new identifier is introduced into the scope. This has to be an unique identifier
        on this scope lvl. But it can overshadow higher scoped (global...) declared variables with the same identifier.
        :return: Amount of errors encountered in node and children.
        """
        ret = True
        self._generate_type_modifier_stack(messenger)
        # We have all the info for the corresponding attribute object
        attr = self._make_attribute()
        # Check of the expression is semantically correct
        if self._expression_node:
            if not self._expression_node.semantic_analysis(messenger):
                return False
            self.analyze_initializer(messenger)

        if self.id and not self._parent_node.add_to_scope_symbol_table(self.id, attr):
            messenger.error_redeclaration(self.id, self._line, self._column)
            ret = False

        return ret

    def analyze_initializer(self, messenger: messages.MessageGenerator):
        """
        Here we will check if the type of the initializer is conform with te type of the declaration
        :return:
        """
        expression_stack = self._expression_node.type_stack
        prev_ele = expression_stack[-1]
        for element in reversed(self._type_stack):

            if expression_stack and element == expression_stack[-1]:
                prev_ele = expression_stack.pop()
            else:
                messenger.warning_init_makes_a_from_b(prev_ele.value,
                                                      self._type_stack[-1].value, self._line, self._column)
                break

        return True
        # TODO mechanism to inform expression node of conversion

    def _make_attribute(self):
        return Attributes.Attributes(self._type_stack, self._line, self._column)

    # LLVM Generation
    # ==================================================================================================================
    def generate_llvm(self, c_comment: bool = True) -> str:
        """
        Generates The llvm code for declaration
        :param bool c_comment: Need to generate C comments?
        :return string: Returns the code string
        """
        # Handling code comments
        expression_c = f' = {self._expression_node}' if self._expression_node else ''
        ret = self.llvm_comment(f'{self._type_stack[0].value} {self.id}{expression_c}', c_comment)

        # Allocate at id
        ret += LlvmCode.llvm_allocate_instruction(self.id, self._type_stack, self.code_indent_string())

        # handle expression node and store it in address of declaration id
        if self._expression_node:
            ret += self._expression_node.generate_llvm_store(self.id)
        return ret
